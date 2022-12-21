"""Top-level module for wtforglib."""

import sys
from os import PathLike
from typing import Any, Dict, TypeVar, Union

KeyType = TypeVar("KeyType")
ValueType = TypeVar("ValueType")


if sys.version_info >= (3, 9):
    Fspec = Union[str, PathLike[str]]
else:
    Fspec = Union[str, "PathLike[str]"]

StrAnyDict = Dict[str, Any]  # type: ignore
