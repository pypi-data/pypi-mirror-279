from abc import abstractmethod
from atom.api import Atom
from cerebrium.utils.files import string_hash
from cerebrium.defaults import (
    MIN_REPLICAS,
    MAX_REPLICAS,
    COOLDOWN,
    CPU,
    MEMORY,
    GPU,
    GPU_COUNT,
    PROVIDER,
    REGION,
    PYTHON_VERSION,
    CUDA_VERSION,
    INCLUDE,
    EXCLUDE,
    SHELL_COMMANDS,
)


class TOMLConfig(Atom):
    @abstractmethod
    def __toml__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __json__(self) -> dict:
        raise NotImplementedError


class ScalingConfig(TOMLConfig):
    min_replicas: int = MIN_REPLICAS
    max_replicas: int = MAX_REPLICAS
    cooldown: int = COOLDOWN

    def __toml__(self) -> str:
        return (
            "[cerebrium.scaling]\n"
            f"min_replicas = {self.min_replicas}\n"
            f"max_replicas = {self.max_replicas}\n"
            f"cooldown = {self.cooldown}\n\n"
        )

    def __json__(self) -> dict:
        return {
            "min_replicas": self.min_replicas,
            "max_replicas": self.max_replicas,
            "cooldown": self.cooldown,
        }


class HardwareConfig(TOMLConfig):
    cpu: int = CPU
    memory: float = MEMORY
    gpu: str = GPU
    gpu_count: int = GPU_COUNT
    provider: str = PROVIDER
    region: str = REGION

    def __toml__(self) -> str:
        return (
            "[cerebrium.hardware]\n"
            f"cpu = {self.cpu}\n"
            f"memory = {self.memory}\n"
            f'gpu = "{self.gpu}"\n'
            f"gpu_count = {self.gpu_count}\n"
            f'provider = "{self.provider}"\n'
            f'region = "{self.region}"\n\n'
        )

    def __json__(self) -> dict:
        return {
            "cpu": self.cpu,
            "memory": self.memory,
            "gpu": self.gpu,
            "gpu_count": self.gpu_count,
            "provider": self.provider,
            "region": self.region,
        }


class DeploymentConfig(TOMLConfig):
    name: str
    python_version: str = PYTHON_VERSION
    cuda_version: str = CUDA_VERSION
    include: str = INCLUDE
    exclude: str = EXCLUDE
    shell_commands: list[str] = SHELL_COMMANDS

    def __toml__(self) -> str:
        return (
            "[cerebrium.deployment]\n"
            f'name = "{self.name}"\n'
            f'python_version = "{self.python_version}"\n'
            f'cuda_version = "{self.cuda_version}"\n'
            f'include = "{self.include}"\n'
            f'exclude = "{self.exclude}"\n'
            f"shell_commands = {self.shell_commands}\n\n"
        )

    def __json__(self) -> dict:
        return {
            "name": self.name,
            "python_version": self.python_version,
            "cuda_version": self.cuda_version,
            "include": self.include,
            "exclude": self.exclude,
            "shell_commands": self.shell_commands,
        }


class DependencyConfig(Atom):
    pip: dict[str, str] = {}
    conda: dict[str, str] = {}
    apt: dict[str, str] = {}

    def __toml__(self) -> str:
        pip_strings = (
            "[cerebrium.dependencies.pip]\n"
            + "\n".join(f'"{key}" = "{value}"' for key, value in self.pip.items())
            + "\n"
            if self.pip
            else ""
        )
        conda_strings = (
            "[cerebrium.dependencies.conda]\n"
            + "\n".join(f'"{key}" = "{value}"' for key, value in self.conda.items())
            + "\n"
            if self.conda != {}
            else ""
        )
        apt_strings = (
            "[cerebrium.dependencies.apt]\n"
            + "\n".join(f'"{key}" = "{value}"' for key, value in self.apt.items())
            + "\n"
            if self.apt != {}
            else ""
        )
        if pip_strings or conda_strings or apt_strings:
            return pip_strings + conda_strings + apt_strings + "\n"
        return ""

    def __json__(self) -> dict:
        return {"pip": self.pip, "conda": self.conda, "apt": self.apt}


class CerebriumConfig(Atom):
    deployment: DeploymentConfig
    hardware: HardwareConfig
    scaling: ScalingConfig
    dependencies: DependencyConfig

    def to_toml(self, file: str = "cerebrium.toml") -> None:
        with open(file, "w") as f:
            f.write(self.deployment.__toml__())
            f.write(self.hardware.__toml__())
            f.write(self.scaling.__toml__())
            f.write(self.dependencies.__toml__())

    def to_payload(self) -> dict:
        hashes = {
            "requirements_hash": string_hash(str(sorted(self.dependencies.pip))),
            "pkglist_hash": string_hash(str(sorted(self.dependencies.apt))),
            "conda_pkglist_hash": string_hash(str(sorted(self.dependencies.conda))),
        }
        payload = {
            **self.deployment.__json__(),
            **self.hardware.__json__(),
            **self.scaling.__json__(),
        }
        payload["hardware"] = payload["gpu"]
        del payload["gpu"]
        payload["region_name"] = payload["region"]
        del payload["region"]
        payload.update(hashes)
        return payload
