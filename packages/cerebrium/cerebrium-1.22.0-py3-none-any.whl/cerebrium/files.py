import os

PREDICT_FILE = "_cerebrium_predict.json"
PIP_REQUIREMENTS_FILE = "requirements.txt"
CONDA_REQUIREMENTS_FILE = "conda_pkglist.txt"
APT_REQUIREMENTS_FILE = "pkglist.txt"
SHELL_COMMANDS_FILE = "shell_commands.sh"
SERVE_SESSION_CACHE_FILE = os.path.join(
    os.path.expanduser("~/.cerebrium"), "serve_session.json"
)

INTERNAL_FILES = [
    PIP_REQUIREMENTS_FILE,
    CONDA_REQUIREMENTS_FILE,
    APT_REQUIREMENTS_FILE,
    PREDICT_FILE,
    SHELL_COMMANDS_FILE,
]
