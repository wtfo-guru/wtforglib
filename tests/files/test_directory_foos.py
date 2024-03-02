"""Test module for wtforglib package."""

import os
import tempfile
from pathlib import Path

import pytest

from wtforglib.files import ensure_directory, verify_directory
from wtforglib.versioned import unlink_path

# mypy: disable_error_code = var-annotated


# ensure_directory tests
def test_exception_raised_ensure():
    """Test raises exception when target exits and is not a directory."""
    t_file, path = tempfile.mkstemp()
    os.close(t_file)
    with pytest.raises(NotADirectoryError):
        ensure_directory(path)
    unlink_path(path, missing_ok=True)


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


# verify_directory tests
def test_verify_directory(tmp_path):
    """Test verify_directory."""
    retval, msg = verify_directory(tmp_path)
    assert retval
    assert msg == "None"


def test_exception_raised_verify():
    """Test raises exception when target exits and is not a directory."""
    t_file, path = tempfile.mkstemp()
    os.close(t_file)
    with pytest.raises(NotADirectoryError):
        verify_directory(path, ex=True)
    unlink_path(path, missing_ok=True)


def test_error_returned_verify():
    """Test raises exception when target exits and is not a directory."""
    t_file, path = tempfile.mkstemp()
    os.close(t_file)
    retval, msg = verify_directory(path)
    assert not retval
    assert msg == "'{0}' is not a directory".format(str(path))
    unlink_path(path, missing_ok=True)
