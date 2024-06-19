import threading
from json.decoder import JSONDecodeError
from requests.exceptions import RequestException
from cerebrium.utils.logging import cerebrium_log
from cerebrium import api


def _graceful_shutdown(
    build_id: str,
    stop_event: threading.Event,
    log_thread: threading.Thread | None,
    is_interrupt: bool = False,
):
    """
    This function is called when the user presses Ctrl+C while streaming logs.
    - stops the spinner
    - sends a kill signal to the backend to stop the build job
    - prints a message
    - exits the program
    """
    stop_event.set()
    if is_interrupt:
        cerebrium_log("\n\nCtrl+C detected. Shutting down current build...", color="yellow")

    try:
        response = api.cerebrium_request(
            http_method="DELETE",
            url="build",
            payload={"buildId": build_id},
        )
        if response is None:
            cerebrium_log(
                message="Error ending build. Please check your internet connection and try again.\nIf the problem persists, please contact support.",
                level="ERROR",
                exit_on_error=False,
            )
            return
        if response.status_code != 200:
            try:
                json_response = response.json()
                if "message" in json_response:
                    cerebrium_log(
                        f"Error ending session: {response.json()['message']}",
                        level="ERROR",
                        exit_on_error=False,
                    )
                return
            except JSONDecodeError:
                cerebrium_log(
                    f"Error ending session{ ':' +response.text if response.text else ''}",
                    level="ERROR",
                    exit_on_error=False,
                )
                return

    except RequestException as e:
        cerebrium_log(f"Error ending session: {e}", level="ERROR", exit_on_error=False)

    if log_thread is not None:
        log_thread.join()
