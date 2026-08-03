"""Top-level module kinds for wtforglib.

The kinds module supports definitions of types used in
the wtforglib package and used in various projects
the author provides.

Types
-----
KeyType
    Generic mapping key type
ValueType
    Generic mapping value type
Fspec
    Fspec = Union[str, PathLike[str]]
Filename
    FSpec
StrAnyDict
    StrAnyDict = Dict[str, Any]
StrStrDict
    StrStrDict = Dict[str, str]
StrStrInt
    StrStrInt = Dict[str, Union[int, str]]
StrStrBool
    StrStrBool = Dict[str, Union[bool, str]]
StrStrIntBool
    StrStrIntBool = Dict[str, Union[int, str, bool]]
StrStrIntBoolNone
    StrStrIntBoolNone = Dict[str, Union[int, str, bool, None]]
"""

from os import PathLike
from typing import Any, TypeVar

KeyType = TypeVar("KeyType")
ValueType = TypeVar("ValueType")

Fspec = str | PathLike[str]

FileName = Fspec

StrAnyDict = dict[str, Any]  # type: ignore
StrStrDict = dict[str, str]
StrStrInt = dict[str, int | str]
StrStrBool = dict[str, bool | str]
StrStrIntBool = dict[str, int | str | bool]
StrStrIntBoolNone = dict[str, int | str | bool | None]
