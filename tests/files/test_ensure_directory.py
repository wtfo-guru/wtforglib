import os
import tempfile
from pathlib import Path

import pytest

from wtforglib.files import ensure_directory

# mypy: disable_error_code = var-annotated


def test_exception_raised():
    """Test raises exception when target exits and is not a directory."""
    _t_file, path = tempfile.mkstemp()
    with pytest.raises(NotADirectoryError):
        ensure_directory(path)
    Path(path).unlink()


def test_directory_exists():
    """Ensure returns True when directory exists."""
    path = tempfile.mkdtemp()
    assert ensure_directory(path)
    Path(path).rmdir()


def test_directory_create():
    """Ensure returns True when directory does not exit."""
    path = tempfile.mkdtemp()
    td = Path(path)
    tp = Path(td.parent, "test_directory.{0}".format(os.getpid()))

    assert ensure_directory(tp)
    assert tp.is_dir()
    td.rmdir()
    tp.rmdir()
