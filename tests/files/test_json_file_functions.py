"""Test module for wtforglib package."""

import os
import tempfile
from pathlib import Path

import pytest

from wtforglib.files import load_json_file, write_json_file
from wtforglib.versioned import unlink_path

test_data = {"foo": "bar"}

# mypy: disable_error_code = var-annotated


def test_write_json_file():
    """Test load_json_file function."""
    _t_file, path = tempfile.mkstemp()
    assert write_json_file(path, test_data)


def test_load_json_file():
    """Test load_json_file function."""
    t_file, path = tempfile.mkstemp()
    os.close(t_file)
    assert write_json_file(path, test_data)
    test_me = load_json_file(path)
    unlink_path(path, missing_ok=True)
    assert isinstance(test_me, dict)
    assert test_me["foo"] == "bar"


def test_load_json_file_missing():
    """Test load_json_file function with missing_ok=False."""
    t_file, path = tempfile.mkstemp()
    os.close(t_file)
    unlink_path(path, missing_ok=True)
    missing_path = str(path) + ".missing"
    with pytest.raises(FileNotFoundError):
        load_json_file(missing_path, False)


def test_load_json_file_directroy():
    """Test load_json_file function passing a directory for file."""
    path = tempfile.mkdtemp()
    with pytest.raises(FileNotFoundError):
        load_json_file(path, False)
    Path(path).rmdir()
