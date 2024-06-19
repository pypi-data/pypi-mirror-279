import json
import os
import re
import tempfile
import time
import zipfile
import jwt
import requests
import yaml
from threading import Event
from datetime import datetime
from typing import Literal
from tenacity import retry, stop_after_delay, wait_fixed
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
from requests.exceptions import ChunkedEncodingError
from time import sleep
from cerebrium.config import CerebriumConfig
from cerebrium.utils.project import get_current_project_context
from cerebrium.utils.logging import cerebrium_log, log_formatted_response, logger
from cerebrium.utils.sync_files import make_cortex_dep_files
from cerebrium.files import INTERNAL_FILES
from cerebrium.types import JSON

ENV = os.getenv("ENV", "prod")
dashboard_url = os.environ.get(
    "DASHBOARD_URL",
    (
        "https://dev-dashboard.cerebrium.ai"
        if ENV == "dev"
        else "https://dashboard.cerebrium.ai"
    ),
)

if ENV == "local":
    api_url = "http://localhost:4100"
elif ENV == "dev":
    api_url = os.getenv("REST_API_URL", "https://dev-rest-api.cerebrium.ai")
else:
    api_url = os.getenv("REST_API_URL", "https://rest-api.cerebrium.ai")

client_id = os.environ.get(
    "CLIENT_ID",
    ("207hg1caksrebuc79pcq1r3269" if ENV in ["dev", "local"] else "2om0uempl69t4c6fc70ujstsuk"),
)

auth_url = os.environ.get(
    "AUTH_URL",
    (
        "https://dev-cerebrium.auth.eu-west-1.amazoncognito.com/oauth2/token"
        if ENV in ["dev", "local"]
        else "https://prod-cerebrium.auth.eu-west-1.amazoncognito.com/oauth2/token"
    ),
)

stream_logs_url = os.environ.get(
    "STREAM_LOGS_URL",
    (
        "https://gklwrtbtdgb4fvs72bw5j2ap3q0omics.lambda-url.eu-west-1.on.aws"
        if ENV == "dev"
        else "https://icnl4trzmhm422rmqbyp4pgniq0uresm.lambda-url.eu-west-1.on.aws"
    ),
)


def is_logged_in() -> str | None:
    """
    Check if a user's JWT token has expired. If it has, make a request to Cognito with the refresh token to generate a new one.

    Returns:
        str: The new JWT token if the old one has expired, otherwise the current JWT token.
    """
    # Assuming the JWT token is stored in a config file
    config_path = os.path.expanduser("~/.cerebrium/config.yaml")
    if not os.path.exists(config_path):
        cerebrium_log(
            level="ERROR",
            message="You must log in to use this functionality. Please run 'cerebrium login'",
            prefix="",
        )
        return None

    with open(config_path, "r") as f:
        config = yaml.safe_load(f) or {}

    if config is None:
        cerebrium_log(
            level="ERROR",
            message="You must log in to use this functionality. Please run 'cerebrium login'",
            prefix="",
        )
        return None

    key_name = "" if ENV == "prod" else f"{ENV}-"

    jwt_token: str = config.get(f"{key_name}accessToken", "")
    refresh_token: str = config.get(f"{key_name}refreshToken", "")
    if not jwt_token:
        cerebrium_log(
            level="ERROR",
            message="You must log in to use this functionality. Please run 'cerebrium login'",
            prefix="",
        )
        return None

    # Decode the JWT token without verification to check the expiration time
    try:
        payload = jwt.decode(jwt_token, options={"verify_signature": False})
    except Exception as e:
        cerebrium_log(level="ERROR", message=f"Failed to decode JWT token: {str(e)}", prefix="")
        return None  # Check if the token has expired
    if datetime.fromtimestamp(payload["exp"]) < datetime.now():
        # Token has expired, request a new one using the refresh token
        response = requests.post(
            auth_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "refresh_token",
                "client_id": client_id,
                "refresh_token": refresh_token,
            },
        )
        if response.status_code == 200:
            new_jwt_token = response.json()["access_token"]
            # Update the config file with the new JWT token
            config[f"{key_name}accessToken"] = new_jwt_token
            with open(config_path, "w") as f:
                yaml.safe_dump(config, f)
            return new_jwt_token
        else:
            cerebrium_log(
                level="ERROR",
                message="Failed to refresh JWT token. Please login again.",
                prefix="",
                exit_on_error=False,
            )
            return None
    else:
        # Token has not expired, return the current JWT token
        return jwt_token


def cerebrium_request(
    http_method: Literal["GET", "POST", "DELETE"],
    url: str,
    payload: dict[str, JSON] = {},
    requires_auth: bool = True,
    stream: bool = False,
    headers: dict[str, str] = {"ContentType": "application/json"},
) -> requests.Response:
    """
    Make a request to the Cerebrium API and check the response for errors.

    Args:
        http_method ('GET', 'POST', 'DELETE'): The HTTP method to use (GET, POST or DELETE).
        url (str): The url after the base url to use.
        payload (dict, optional): The payload to send with the request.
        requires_auth (bool): If the api call requires the user to be authenticated
        stream (bool): If the request is to a streaming endpoint
        headers (dict, optional): By default, content-type is application/json so this is used to override

    Returns:
        dict: The response from the request.
    """
    if requires_auth:
        access_token = is_logged_in()
        if not access_token:
            raise Exception("User is not logged in")

        payload["projectId"] = get_current_project_context()

    else:
        access_token = None
    url = f"{stream_logs_url}/{url}" if stream else f"{api_url}/{url}"

    if access_token:
        headers["Authorization"] = f"{access_token}"

    @retry(stop=stop_after_delay(60), wait=wait_fixed(8))
    def _request():
        data = None if payload is None else json.dumps(payload)
        if http_method == "POST":
            response = requests.post(url, headers=headers, data=data, timeout=30)
        elif http_method == "GET":
            response = requests.get(
                url,
                headers=headers,
                params=payload,
                stream=stream,
                timeout=None if stream else 30,
            )
        else:
            response = requests.delete(
                url, headers=headers, params=payload, data=data, timeout=30
            )
        return response

    response = _request()

    return response


def get_build_status(build_id: str, mode: Literal["build"] | Literal["serve"] = "build") -> str:
    """Get the build status of a build from the backend"""
    build_status_response = cerebrium_request(
        "GET",
        f"getBuildStatus?buildId={build_id}",
        {},
    )

    if build_status_response is None:
        cerebrium_log(
            level="ERROR",
            message=f"Error getting {mode} status. Please check your internet connection and ensure you are logged in.\n If this issue persists, please contact support.",
        )
        exit()

    if build_status_response.status_code != 200:
        cerebrium_log(
            level="ERROR",
            message=f"Error getting {mode} status\n{build_status_response.json()['message']}",
            prefix="",
        )

    return build_status_response.json()["status"]


def upload_cortex_files(
    upload_url: str,
    zip_file_name: str,
    config: CerebriumConfig,
    file_list: list[str],
    source: Literal["serve", "cortex"] = "cortex",
    disable_animation: bool = False,
) -> bool:
    if file_list == []:
        cerebrium_log(
            level="ERROR",
            message="No files to upload.",
            prefix="Error uploading app to Cerebrium:",
        )
        return False

    # Zip all files in the current directory and upload to S3
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, zip_file_name)
        make_cortex_dep_files(working_dir=temp_dir, config=config)
        tmp_dep_files = os.listdir(temp_dir)
        with zipfile.ZipFile(zip_path, "w") as zip_file:
            print(f"🗂️  Zipping {len(file_list)} file(s)...")
            for f in tmp_dep_files:
                if not disable_animation:
                    print(f"⥅ Creating dependency file {f}")
                zip_file.write(os.path.join(temp_dir, f), arcname=os.path.basename(f))

            for f in file_list:
                if os.path.basename(f) in INTERNAL_FILES:
                    if not disable_animation:
                        print(f"⛔️ Skipping conflicting dependency file {f}")
                        print(
                            f"ℹ  Ensure dependencies in `{f}` are reflected in `cerebrium.toml`"
                        )
                    continue
                if not disable_animation:
                    print(f"＋ Adding {f}")
                if os.path.isfile(f):
                    zip_file.write(f)
                elif os.path.isdir(f) and len(os.listdir(f)) == 0:
                    zip_file.write(f, arcname=os.path.basename(f))

        print("⬆️  Uploading to Cerebrium...")

        with open(zip_path, "rb") as f:
            headers = {
                "Content-Type": "application/zip",
            }
            if not disable_animation:
                with tqdm(
                    total=os.path.getsize(zip_path),
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    colour="#EB3A6F",
                ) as pbar:  # type: ignore
                    wrapped_f = CallbackIOWrapper(pbar.update, f, "read")
                    upload_response = requests.put(
                        upload_url,
                        headers=headers,
                        data=wrapped_f,  # type: ignore
                        timeout=60,
                        stream=True,
                    )
            else:
                upload_response = requests.put(
                    upload_url,
                    headers=headers,
                    data=f,
                    timeout=60,
                    stream=True,
                )

        if upload_response.status_code != 200:
            cerebrium_log(
                level="ERROR",
                message=f"Error uploading app to Cerebrium\n{upload_response.json().get('message')}",
                prefix="",
            )
            return False
        if source == "cortex":
            print("✅ Resources uploaded successfully.")
        return True


def log_build_status(
    build_status: str,
    start_time: float,
    mode: Literal["build"] | Literal["serve"] = "build",
) -> str:
    # Status messages mapping
    status_messages = {
        "building": "🔨 Building App...",
        "initializing": "🛠️ Initializing...",
        "synchronizing_files": "📂 Syncing files...",
        "serving": "⏰ Waiting for requests...",
        "pending": "⏳ Build pending...",
        "failed": "🚨 Build failed!",
    }

    # Default message
    msg = status_messages.get(build_status, str(build_status).replace("_", " ").capitalize())
    if build_status == "None":
        msg = "waiting for build status..."

    if build_status == "Success" and mode == "serve":
        msg = "⏰ Waiting for requests..."

    if build_status == "pending" and time.time() - start_time > 20:
        msg = "⏳ Build pending...trying to find hardware"

    return msg


def stream_logs(
    start_event: Event,
    stop_event: Event,
    modelId: str,
    buildId: str,
):
    """

    Hits a streaming logging endpoint and prints out the logs.

    Args:
        start_event (threading event): Lets thread know that it has started receiving logs.
        stop_event (threading event): Lets thread know that it should stop processing
        modelId (str): The unique identifier of the model you would like to see streamed logs for
        buildId (str): The unique identifier of the build you would like to see streamed logs for
    """
    try:
        headers = {
            "Content-Type": "text/event-stream",
            "Transfer-Encoding": "chunked",
            "Connection": "keep-alive",
        }

        response = cerebrium_request(
            "GET",
            f"?modelId={modelId}&buildId={buildId}",
            {},
            headers=headers,
            stream=True,
        )
        if response.status_code != 200:
            logger.error(f"Failed to stream logs. Status code: {response.status_code}")
            exit()
    except Exception as e:
        logger.error(f"An error occurred while streaming logs: {e}")
        exit()

    iterator = response.iter_lines()
    index = 0
    while not stop_event.is_set():
        try:
            line = next(iterator)
            index += 1
            if line:
                decoded_line = line.decode("utf-8")
                log_formatted_response(decoded_line)
                if not start_event.is_set():
                    start_event.set()
        except ChunkedEncodingError:
            logger.warning("Connection broken. Retrying...")
            sleep(5)
            response = cerebrium_request(
                "GET",
                f"?modelId={modelId}&buildId={buildId}",
                {},
                headers=headers,
                stream=True,
            )
            iterator = response.iter_lines()
            for _ in range(index):
                next(iterator)
            if response.status_code != 200:
                logger.error(f"Failed to stream logs. Status code: {response.status_code}")
                break
        except StopIteration:
            logger.debug("Connection closed.")
        except Exception as e:
            logger.error(f"An error occurred while streaming logs: {e}")
            break


def poll_build_logs(
    buildId: str,
    start_event: Event,
    stop_event: Event,
    mode: Literal["build", "serve"] = "build",
    interval: int = 2,
):
    """
    Polls logs at specified intervals and prints only new log lines.

    Args:
        buildId (str, optional): The unique identifier of the build you would like to see streamed logs for
        start_event (threading event): Lets thread know that it has started receiving logs.
        stop_event (threading event): Lets thread know that it should stop processing
        interval (int): The interval in seconds between polls. Defaults to 2 seconds.
    """
    last_seen_logs: list[str] = []
    while not stop_event.is_set():
        logs_response = cerebrium_request("GET", f"streamBuildLogs?{mode}Id={buildId}", {})
        if logs_response is None:
            stop_event.set()
            cerebrium_log(
                level="ERROR",
                message="Error streaming logs. Please check your internet connection and ensure you are logged in. If this issue persists, please contact support.",
            )
            exit()

        if logs_response.status_code == 200:
            # Concatenate the log parts into a single string
            concatenated_logs = "".join(logs_response.json()["logs"])
            # Use a regular expression to split the concatenated string into lines at timestamps
            # Assuming ISO 8601 format for timestamps: 2024-02-05T21:12:05.650831712Z
            current_log_lines = re.split(
                r"(?=\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z)", concatenated_logs
            )

            # Process each log line
            for line in current_log_lines:
                if line and line not in last_seen_logs and not line.isspace():
                    log_formatted_response(
                        line
                    )  # we should always receive some type of log so wait until this happens
                    start_event.set()
                    last_seen_logs.append(line)  # Add the new line to the list of seen logs

        # else:
        #     print(f"Failed to fetch logs. Status code: {logs_response.status_code}")
        time.sleep(interval)
