from os import PathLike
from typing import Any, TypeVar, Union

KeyType = TypeVar("KeyType")
ValueType = TypeVar("ValueType")

Fspec = Union[str, PathLike[str]]
Wdict = dict[Any, Any]  # type: ignore
