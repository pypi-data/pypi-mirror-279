from typing import Literal, TypedDict, TypeAlias
from collections.abc import Mapping

LogLevel = Literal["DEBUG", "INFO", "ERROR", "INTERNAL", "WARNING"]
JSON: TypeAlias = Mapping[str, "JSON"] | str | int | float | bool | None


class FileData(TypedDict):
    fileName: str
    hash: str
    dateModified: float
    size: int
