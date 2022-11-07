import errno
import os
from typing import Union


def raise_filenotfound(filenm: Union[str, os.PathLike[str]]) -> None:
    """Raised a FileNotFoundError execption for the given filenm"""
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filenm)
