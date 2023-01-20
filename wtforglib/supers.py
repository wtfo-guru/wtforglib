"""Top-level module for wtforglib Library."""

# vim:ft=py noqa: E800
import platform

from wtforglib.functions import WINDOZE

if platform.system() == WINDOZE:
    from ctypes.windll.shell32 import IsUserAnAdmin  # noqa: WPS433

    SUPER = "Administrator"
else:
    from os import geteuid  # noqa: WPS433

    SUPER = "super user"


class AdminStateUnknownError(Exception):
    """Cannot determine whether the user is an admin."""


def issuper() -> bool:
    """Return True/False depending on process euid.

    Returns
    -------
        bool : true if process euid is 0

    Raises
    ------
    AdminStateUnknownError
        When if platform is Windows
    """
    try:
        if platform.system() == WINDOZE:
            return IsUserAnAdmin() == 1
        return geteuid() == 0
    except AttributeError:
        raise AdminStateUnknownError()


def requires_super_user(prefix: str = "Specified action") -> None:
    """Raises exception if process isn't euid 0.

    Parameters
    ----------
    prefix : str
        Text to prefix to exception message

    Raises
    ------
    PermissionError
        if process euid is not 0
    """
    if not issuper():  # pragma no cover
        raise PermissionError("{0} requires {1} priviledges!".format(prefix, SUPER))
