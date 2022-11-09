import errno
import os
from typing import Union


def raise_filenotfound(filenm: Union[str, os.PathLike[str]]) -> None:
    """Raises a FileNotFoundError execption for the given filenm.

    Parameters
    ----------
    filenm : Union[str,PathLike[str]]
        The yaml file to load

    Raises
    ------
    FileNotFoundError
        If fail_missing is True and filenm does not exist
    """
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filenm)
