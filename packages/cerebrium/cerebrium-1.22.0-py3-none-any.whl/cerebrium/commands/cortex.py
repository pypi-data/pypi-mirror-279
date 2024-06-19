import os
import re
import sys
import typer
import toml
import cProfile
from pstats import Stats
from typing import Annotated
from rich import print as console
from rich.console import Group
from rich.panel import Panel
from rich.text import Text
from termcolor import colored
from cerebrium import api
from cerebrium.core import cli
from cerebrium.config import (
    CerebriumConfig,
    ScalingConfig,
    HardwareConfig,
    DeploymentConfig,
    DependencyConfig,
)
from cerebrium.utils.logging import cerebrium_log
from cerebrium.utils.requirements import strip_delimiters
from cerebrium.utils.deploy import package_app
from cerebrium import defaults


_EXAMPLE_MAIN = """
def run(param_1: str, param_2: str, run_id):  # run_id is optional, injected by Cerebrium at runtime
    my_results = {"1": param_1, "2": param_2}
    my_status_code = 200 # if you want to return a specific status code

    return {"my_result": my_results, "status_code": my_status_code} # return your results
"""


@cli.command("init")
def init(
    name: Annotated[str, typer.Argument(help="Name of the Cortex deployment.")],
    pip: Annotated[
        str,
        typer.Option(
            help=(
                "Optional list of requirements. "
                "Example: \"['transformers', 'torch==1.31.1']\""
            ),
        ),
    ] = "[]",
    apt: Annotated[
        str,
        typer.Option(
            help=("Optional list of apt packages. For example: \"['git', 'ffmpeg' ]\""),
        ),
    ] = "[]",
    conda: Annotated[str, typer.Option(help="Optional list of conda packages.")] = "[]",
    cpu: Annotated[
        int,
        typer.Option(
            help=(
                "Number of vCPUs (cores) to use for the Cortex deployment. " "Defaults to 3."
            ),
        ),
    ] = defaults.CPU,
    memory: Annotated[
        float,
        typer.Option(
            help=(
                "Amount of memory (in GB) to use for the Cortex deployment. "
                "Defaults to 14.0GB. "
            ),
        ),
    ] = defaults.MEMORY,
    gpu: Annotated[
        str,
        typer.Option(
            help=("Type of GPU to use for the Cortex deployment. " "Defaults to 'AMPERE_A10'."),
        ),
    ] = defaults.GPU,
    gpu_count: Annotated[
        int,
        typer.Option(
            help=("Number of GPUs to use for the Cortex deployment. " "Defaults to 1."),
        ),
    ] = defaults.GPU_COUNT,
    include: Annotated[
        str,
        typer.Option(
            help=(
                "Comma delimited string list of relative paths to files/folder to include. "
                "Defaults to all visible files/folders in project root."
            ),
        ),
    ] = defaults.INCLUDE,
    exclude: Annotated[
        str,
        typer.Option(
            help=(
                "Comma delimited string list of relative paths to files/folder to exclude. "
                "Defaults to all hidden files/folders in project root."
            ),
        ),
    ] = defaults.EXCLUDE,
    python_version: Annotated[
        str,
        typer.Option(
            help=("Python version to use. Defaults to the current interpreter version."),
        ),
    ] = defaults.PYTHON_VERSION,
    cuda_version: Annotated[
        str,
        typer.Option(
            help=("CUDA version to use. " "Defaults to '12'"),
        ),
    ] = defaults.CUDA_VERSION,
    min_replicas: Annotated[
        int,
        typer.Option(
            help=("Minimum number of replicas to keep running. " "Defaults to 0."),
        ),
    ] = defaults.MIN_REPLICAS,
    max_replicas: Annotated[
        int,
        typer.Option(
            help=("Maximum number of replicas to keep running. " "Defaults to 5."),
        ),
    ] = defaults.MAX_REPLICAS,
    cooldown: Annotated[
        int,
        typer.Option(
            help=("Cooldown period in seconds. " "Defaults to 60 seconds (5 minutes)."),
        ),
    ] = defaults.COOLDOWN,
):
    """
    Initialize an empty Cerebrium Cortex project.
    """
    print(f"Initializing Cerebrium Cortex project in {name}")

    if not os.path.exists(name):
        os.makedirs(name)
    else:
        cerebrium_log(
            level="WARNING",
            message="Directory already exists. Please choose a different name.",
            prefix_seperator="\t",
        )
        raise typer.Exit()

    if not os.path.exists(os.path.join(name, "main.py")):
        with open(os.path.join(name, "main.py"), "w") as f:
            f.write(_EXAMPLE_MAIN)

    pip_dict = strip_delimiters(pip)
    apt_dict = strip_delimiters(apt)
    conda_dict = strip_delimiters(conda)

    scaling_config = ScalingConfig(
        min_replicas=min_replicas, max_replicas=max_replicas, cooldown=cooldown
    )
    hardware_config = HardwareConfig(
        cpu=cpu,
        memory=memory,
        gpu=gpu,
        gpu_count=gpu_count,
        provider=defaults.PROVIDER,
        region=defaults.REGION,
    )
    dependency_config = DependencyConfig(pip=pip_dict, apt=apt_dict, conda=conda_dict)
    deployment_config = DeploymentConfig(
        name=name,
        python_version=python_version,
        cuda_version=cuda_version,
        include=include,
        exclude=exclude,
        shell_commands=defaults.SHELL_COMMANDS,
    )
    config = CerebriumConfig(
        scaling=scaling_config,
        hardware=hardware_config,
        deployment=deployment_config,
        dependencies=dependency_config,
    )
    config.to_toml(f"{name}/cerebrium.toml")
    print("🚀 Cerebrium Cortex project initialized successfully!")


@cli.command("deploy")
def deploy(
    disable_syntax_check: Annotated[
        bool, typer.Option(help="Flag to disable syntax check.")
    ] = False,
    force_rebuild: Annotated[
        bool,
        typer.Option(
            help="Force rebuild an app. Clears a deployment's environment and builds as if it is a clean deployment.",
        ),
    ] = False,
    init_debug: Annotated[
        bool,
        typer.Option(
            help="Pauses the container after initialization. You need to manually cancel the build to terminate.",
        ),
    ] = False,
    log_level: Annotated[
        str,
        typer.Option(
            help="Log level for the Cortex deployment. Can be one of 'DEBUG' or 'INFO'",
        ),
    ] = "INFO",
    config_file: Annotated[
        str,
        typer.Option(
            help="Path to the cerebrium config TOML file. You can generate a config using `cerebrium init`."
        ),
    ] = "./cerebrium.toml",
    disable_confirmation: Annotated[
        bool,
        typer.Option(
            "--disable-confirmation",
            "-y",
            help="Disable the confirmation prompt before deploying.",
        ),
    ] = False,
    disable_animation: Annotated[
        bool,
        typer.Option(
            "--disable-animation",
            help="Disable TQDM loading bars and yaspin animations.",
        ),
    ] = False,
    disable_build_logs: Annotated[
        bool,
        typer.Option("--disable-build-logs", help="Disable build logs during a deployment."),
    ] = False,
):
    """
    Deploy a Cortex deployment to Cerebrium
    """

    with cProfile.Profile() as pr:
        # load config toml file
        log_level = log_level.upper()
        assert log_level in [
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "INTERNAL",
        ], "Log level must be one of 'DEBUG' or 'INFO'"
        try:
            toml_config = toml.load(config_file)["cerebrium"]
        except FileNotFoundError:
            cerebrium_log(
                message="Could not find cerebrium.toml file. Please run `cerebrium init` to create one.",
                color="red",
            )
            raise typer.Exit()
        except KeyError:
            cerebrium_log(
                message="Could not find 'cerebrium' key in cerebrium.toml file. Please run `cerebrium init` to create one.",
                color="red",
            )
            raise typer.Exit()
        except Exception as e:
            cerebrium_log(message=f"Error loading cerebrium.toml file: {e}", color="red")
            raise typer.Exit()

        deployment_section = toml_config.get("deployment", {})
        if not deployment_section:
            cerebrium_log(
                message="Deployment section is required in cerebrium.toml file. Please add a 'deployment' section.",
                color="red",
            )
            raise typer.Exit()
        if "name" not in deployment_section:
            cerebrium_log(
                message="`deployment.name` is required in cerebrium.toml file. Please add a 'name' field to the 'deployment' section.",
                color="red",
            )
            raise typer.Exit()
        deployment_config: DeploymentConfig = DeploymentConfig(**deployment_section)
        scaling_config: ScalingConfig = ScalingConfig(**toml_config.get("scaling", {}))
        hardware_config: HardwareConfig = HardwareConfig(**toml_config.get("hardware", {}))
        dependency_config: DependencyConfig = DependencyConfig(
            **toml_config.get("dependencies", {})
        )
        config: CerebriumConfig = CerebriumConfig(
            scaling=scaling_config,
            hardware=hardware_config,
            deployment=deployment_config,
            dependencies=dependency_config,
        )

        # Check if the provider is Coreweave, if so print a V3 deprecation warning
        if config.hardware.provider == "coreweave":
            cerebrium_log(
                message="WARNING: Cortex V4 does not currently support Coreweave. Please considering updating your deployment to V4 and deploying to AWS.",
                level="WARNING",
            )
        build_status, setup_response = package_app(
            config,
            "deploy",
            force_rebuild,
            init_debug,
            disable_build_logs,
            log_level,  # type: ignore
            disable_syntax_check,
            disable_animation,
            disable_confirmation,
        )
        if setup_response is None:
            cerebrium_log(
                message="Error setting up your deployment and getting your logs. Please check your dashboard or contact support if the issue persists.",
                color="red",
            )
            sys.exit(1)
        if "success" == build_status:
            project_id = setup_response["projectId"]
            jwt = setup_response["jwt"]
            endpoint = setup_response["internalEndpoint"]

            dashboard_url = f"{api.dashboard_url}/projects/{project_id}/models/{project_id}-{config.deployment.name}"

            info_string = (
                f"🔗 [link={dashboard_url}]View your deployment dashboard here[/link]\n"
                f"🔗 [link={dashboard_url}?tab=builds]View builds here[/link]\n"
                f"🔗 [link={dashboard_url}?tab=runs]View runs here[/link]\n\n"
                f"🛜  Endpoint:\n{endpoint}"
            )

            dashboard_info = Panel(
                info_string,
                title=f"[bold green]🚀 {config.deployment.name} is now live! 🚀 ",
                border_style="green",
                width=100,
                padding=(1, 2),
            )

            console(Group(dashboard_info))

            curl_command = colored(
                f"curl -X POST {endpoint}/{{function}} \\\n"
                "     -H 'Content-Type: application/json'\\\n"
                f"     -H 'Authorization: Bearer {jwt}'\\\n"
                '     --data \'{"param": "Hello World!"}\'',
                "green",
            )
            print(
                "\n💡You can call the endpoint with the following curl command:\n"
                f"{curl_command}"
            )
        elif build_status in ["build_failure", "init_failure"]:
            console(
                Text(
                    "Unfortunately there was an issue with your deployment",
                    style="red",
                )
            )
    pr.disable()
    if log_level == "INTERNAL":
        stats = Stats(pr)
        stats.sort_stats("tottime").print_stats(10)
