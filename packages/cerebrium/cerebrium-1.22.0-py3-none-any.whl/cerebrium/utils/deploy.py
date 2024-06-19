import os
import sys
import threading
import time
import typer
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text
from typing import Any, Literal
from cerebrium import __version__
from cerebrium.api import (
    cerebrium_request,
    upload_cortex_files,
    get_build_status,
    log_build_status,
    poll_build_logs,
    stream_logs,
)
from cerebrium.config import CerebriumConfig
from cerebrium.types import LogLevel
from cerebrium.utils.logging import cerebrium_log, console
from cerebrium.utils.termination import _graceful_shutdown
from cerebrium.utils.files import determine_includes, file_hash
from cerebrium.utils.display import confirm_deployment
from cerebrium.utils.verification import run_pyflakes

ENV = os.getenv("ENV", "prod")


def _setup_request(
    payload: dict,
) -> dict[str, Any]:
    setup_response = cerebrium_request("POST", "setupApp", payload)
    if setup_response is None:
        cerebrium_log(
            level="ERROR",
            message="❌ There was an error deploying your app. Please login and try again. If the error continues to persist, contact support.",
            prefix="",
        )
        exit()

    if setup_response.status_code != 200:
        cerebrium_log(
            message=f"❌ There was an error deploying your app\n{setup_response.json()['message']}",
            prefix="",
            level="ERROR",
        )
        exit()
    print("✅ App setup complete!")

    return setup_response.json()


def package_app(
    config: CerebriumConfig,
    app_type: Literal["deploy", "serve"],
    force_rebuild: bool,
    init_debug: bool,
    disable_build_logs: bool,
    log_level: LogLevel,
    disable_syntax_check: bool,
    disable_animation: bool,
    disable_confirmation: bool,
):
    # Get the files in the users directory
    file_list = determine_includes(
        include=config.deployment.include,
        exclude=config.deployment.exclude,
    )
    if file_list == []:
        cerebrium_log(
            "⚠️ No files to upload. Please ensure you have files in your project.",
            level="ERROR",
        )
        raise typer.Exit()

    if "./main.py" not in file_list and "main.py" not in file_list:
        cerebrium_log(
            "⚠️ main.py not found. Please ensure your project has a main.py file.",
            level="ERROR",
        )
        raise typer.Exit()

    if not disable_syntax_check:
        run_pyflakes(files=file_list, print_warnings=True)

    if not disable_confirmation:
        if not confirm_deployment(config):
            sys.exit()

    # If files are larger than 10MB, use partial_upload otherwise upload with app zip
    partial_upload = False
    # if check_deployment_size(file_list, 10) or len(file_list) > 500:
    #     if len(file_list) < 1000:
    #         cerebrium_log(
    #             "📦 Large upload, only uploading files that have changed...",
    #             level="INFO",
    #         )
    #         partial_upload = True
    #     else:
    #         cerebrium_log(
    #             "⚠️ 1000+ files detected. Partial sync not possible. Try reduce the number of files or file size for faster deployments.",
    #             level="ERROR",
    #         )
    #         return "Failed to deploy", None

    payload = config.to_payload()
    payload["function"] = app_type
    payload["force_rebuild"] = force_rebuild
    payload["init_debug"] = init_debug
    payload["log_level"] = log_level
    payload["disable_build_logs"] = disable_build_logs
    payload["upload_hash"] = file_hash(file_list)
    payload["cerebrium_version"] = __version__

    # if partial_upload:
    #     setup_response = _partial_upload(
    #         cerebrium_config=config,
    #         source=app_type,
    #         file_list=file_list,
    #         force_rebuild=force_rebuild,
    #         disable_animation=disable_animation,
    #     )
    # else:
    setup_response = _setup_request(
        payload,
    )

    build_id = setup_response["buildId"]
    print(f"🆔 Build ID: {build_id}")
    build_status = str(setup_response["status"])

    if build_status == "pending":
        if not partial_upload:
            upload_cortex_files(
                upload_url=setup_response["uploadUrl"],
                zip_file_name=os.path.basename(setup_response["keyName"]),
                config=config,
                file_list=file_list,
                disable_animation=disable_animation,
            )

    build_status = _stream_logs(
        build_id=build_id,
        cerebrium_config=config,
        setup_response=setup_response,
        build_status=build_status,
        disable_animation=disable_animation,
    )

    return build_status, setup_response


def _stream_logs(
    build_id: str,
    cerebrium_config: CerebriumConfig,
    setup_response: dict[str, Any],
    build_status: str,
    disable_animation: bool = False,
):
    spinner = None
    if build_status == "pending":
        build_status = "Build pending..."
        start_time = time.time()
        spinner = (
            None if disable_animation else Spinner("dots", "Building App...", style="gray")
        )

        # This is used to stop the logs on a different thread
        start_event = threading.Event()
        stop_event = threading.Event()

        if ENV == "local":
            log_thread = threading.Thread(
                target=poll_build_logs,
                args=(
                    setup_response["buildId"],
                    start_event,
                    stop_event,
                ),
            )
        else:
            log_thread = threading.Thread(
                target=stream_logs,
                args=(
                    start_event,
                    stop_event,
                    f'{setup_response["projectId"]}-{cerebrium_config.deployment.name}',
                    setup_response["buildId"],
                ),
            )

        log_thread.start()
        live = Live(spinner, console=console, refresh_per_second=10)

        # Start the Live context using the start() method
        live.start()
        build_status = ""
        try:
            while True:
                old_build_status = build_status
                build_status = get_build_status(setup_response["buildId"])
                if spinner:
                    spinner.text = log_build_status(build_status, start_time)
                elif old_build_status != build_status:
                    print(log_build_status(build_status, start_time, mode="build"))

                if build_status in ["success", "build_failure", "init_failure"]:
                    start_event.wait()
                    live.update(Text(""))
                    stop_event.set()
                    break
                time.sleep(5)
        except KeyboardInterrupt:
            # If user presses Ctrl-C, signal all threads to stop
            live.stop()
            _graceful_shutdown(
                build_id=build_id,
                stop_event=stop_event,
                log_thread=log_thread,
                is_interrupt=True,
            )
        finally:
            # Stop the Live instance after the loop
            live.stop()
        log_thread.join()
    elif build_status == "running":
        print("🤷 No file changes detected. Not fetching logs")
    else:
        if spinner:
            spinner.stop(text="Build failed")
        cerebrium_log("ERROR", "Build failed.")

    return build_status


# def _partial_upload(
#     cerebrium_config: CerebriumConfig,
#     source: Literal["deploy", "serve"],
#     file_list: list[str],
#     force_rebuild: bool,
#     disable_animation,
# ) -> dict[str, Any]:
#     """
#     Partial uploads need to be done in a different flow to the normal upload.
#
#     This function will:
#     - Create all utility files (requirements.txt, apt.txt, conda.txt, _cerebrium_predict.json, etc) and remove any conflicting files
#     - Get the hashes of all the files
#     - Compare the hashes to the hashes of the last deployment
#     - Upload the files that have changed
#     - Create a marker file with the hashes of the new files
#
#     """
#     temp_file_list: list[str] = file_list.copy()
#
#     # make utility files
#     sync_files.make_cortex_util_files(working_dir=os.getcwd(), config=cerebrium_config)
#     current_dir_files = os.listdir(os.getcwd())
#
#     temp_file_list.extend(
#         [f for f in INTERNAL_FILES if f in current_dir_files],
#     )
#     local_files = sync_files.gather_hashes(temp_file_list)
#
#     params = flatten_cerebrium_config_to_json(config=cerebrium_config)
#     params["function"] = source
#
#     setup_response = _setup_request(
#         config, params, file_list, force_rebuild, disable_animation
#     )
#
#     if setup_response["status"] == "pending":
#         uploaded_count = upload_files_to_s3(
#             setup_response["uploadUrls"], quiet=disable_animation
#         )
#         upload_marker_file_and_delete(
#             setup_response["markerFile"],
#             uploaded_count,
#             setup_response["buildId"],
#             local_files,
#         )
#
#     return setup_response
