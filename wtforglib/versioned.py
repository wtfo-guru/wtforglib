"""Top-level module for wtforglib."""

from pathlib import Path

from wtforglib.kinds import Fspec


def unlink_path(fspec: Fspec, missing_ok: bool = False) -> None:
    """Unlink file with version support.

    Parameters
    ----------
    fspec : Fspec
        Specification of file to unlink
    missing_ok : bool
        Flag to specify if file must exist

    Raises
    ------
    FileNotFoundError
        If missing_ok is False and file does not exist.
    """
    path = Path(fspec)
    try:
        path.unlink()
    except FileNotFoundError:
        if not missing_ok:
            raise
