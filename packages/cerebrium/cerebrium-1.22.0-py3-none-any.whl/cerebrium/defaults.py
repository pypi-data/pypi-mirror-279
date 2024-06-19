from sys import version_info

# Deployment
PYTHON_VERSION = f"{version_info.major}.{version_info.minor}"
CUDA_VERSION = "12"
INCLUDE = "[./*, main.py, cerebrium.toml]"
EXCLUDE = "[.*]"
SHELL_COMMANDS = []

# Hardware
CPU = 3
MEMORY = 14.0
GPU = "AMPERE_A10"
GPU_COUNT = 1
PROVIDER = "aws"
REGION = "us-east-1"

# Scaling
MIN_REPLICAS = 0
MAX_REPLICAS = 5
COOLDOWN = 60
