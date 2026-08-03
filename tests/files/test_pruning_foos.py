"""Module to create a tree structure for testing directory functions."""

import os
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from wtforglib.dirs import (
    delete_empty_dirs,
    prune_older_files,
    prune_older_files_empty_dir,
)
from wtforglib.functions import local_tz

STEP = 27
DIR_NAMES = (
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
)


def _set_days_earlier(fp: Path, days: int) -> None:
    """Set access, modification date to days earlier.

    Parameters
    ----------
    fp : Path
        Path to the file to be changed
    days : int
        Number of days earlier to set dates
    """
    ltz = local_tz()
    fs = os.stat(fp)
    dt = datetime.fromtimestamp(fs.st_mtime, ltz) - timedelta(days=days)
    dt = dt - timedelta(days=days)
    ts = dt.timestamp()
    os.utime(fp, times=(ts, ts))


def _initialize_tree() -> str:
    """Initialize the test tree structure."""
    top: str | Path = tempfile.mkdtemp()
    print(f"type: {type(top)!s}, value: {top}")
    top = Path(top)
    # tree = top / "one" / "two" / "three" / "four" / "five"
    # tree.mkdir(parents=True, exist_ok=True)
    # tree = top / "six" / "seven" / "eight" / "nine" / "ten"
    # tree.mkdir(parents=True, exist_ok=True)
    td = top
    days = STEP
    for sd in DIR_NAMES:
        if sd == "six":
            td = top
        td = td / sd  # noqa: WPS350
        td.mkdir(parents=True, exist_ok=True)
        tf = td / f"{sd}.txt"
        tf.touch()
        if days % 2 == 0:
            _set_days_earlier(tf, days)
        days += STEP
    return str(top)


def _cleanup(tree_top: str) -> None:
    """Cleanup the test tree structure."""
    # Delete everything reachable from the directory "top".
    # CAUTION:  This is dangerous! For example, if top == Path('/'),
    # it could delete all of your files.
    if tree_top in {"/", "/home", "/root", "/etc", "/usr", "/var"}:
        raise ValueError(f"Invalid tree top: {tree_top}")
    top = Path(tree_top)
    for root, dirs, files in os.walk(top, topdown=False):
        rp = Path(root)
        for fn in files:
            (rp / fn).unlink()
        for dn in dirs:
            (rp / dn).rmdir()
    top.rmdir()


def test_prune_older_empty_foos() -> None:
    """Run the test."""
    top = _initialize_tree()
    pruned = prune_older_files(top, 3 * STEP)
    assert pruned == 5
    pruned = delete_empty_dirs(top)
    assert pruned == 1
    _cleanup(str(top))


def test_prune_older_empty_dir_foo() -> None:
    """Run the test."""
    top = _initialize_tree()
    pruned = prune_older_files_empty_dir(top, 3 * STEP)
    assert pruned == 6
