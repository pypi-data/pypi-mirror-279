import yaml
import os


def get_current_project_context() -> str | None:
    """
    Get the current project context and project name
    """
    config_path = os.path.expanduser("~/.cerebrium/config.yaml")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            env = os.getenv("ENV", "prod")
            key_prefix = "" if env == "prod" else f"{env}-"
            if config.get(f"{key_prefix}project"):
                return config.get(f"{key_prefix}project")
    print("No current project context found.")
    return None
