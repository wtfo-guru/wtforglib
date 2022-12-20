from os import PathLike
from typing import Any, Dict, TypeVar, Union

KeyType = TypeVar("KeyType")
ValueType = TypeVar("ValueType")

Fspec = Union[str, PathLike[str]]
Wdict = Dict[Any, Any]  # type: ignore
StrAnyDict = Dict[str, Any]  # type: ignore
