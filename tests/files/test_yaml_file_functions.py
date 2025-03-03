"""Test module for wtforglib package."""

import os
import tempfile
from pathlib import Path

import pytest

from wtforglib.files import (
    WRITE_YAML_DEPRECATED,
    load_yaml_file,
    safe_write_yaml_file,
    write_yaml_file,
)
from wtforglib.versioned import unlink_path

# mypy: disable_error_code = var-annotated


def test_load_yaml_file():
    """Test load_yaml_file function."""
    t_file, path = tempfile.mkstemp()
    os.close(t_file)
    assert safe_write_yaml_file(path, {"foo": "bar"})
    test_me = load_yaml_file(path)
    unlink_path(path, missing_ok=True)
    assert isinstance(test_me, dict)
    assert test_me["foo"] == "bar"


def test_load_yaml_file_missing():
    """Test load_yaml_file function with missing_ok=False."""
    t_file, path = tempfile.mkstemp()
    os.close(t_file)
    unlink_path(path, missing_ok=True)
    missing_path = str(path) + ".missing"
    with pytest.raises(FileNotFoundError):
        load_yaml_file(missing_path, False)


def test_load_yaml_file_directroy():
    """Test load_yaml_file function passing a directory for file."""
    path = tempfile.mkdtemp()
    with pytest.raises(FileNotFoundError):
        load_yaml_file(path, False)
    Path(path).rmdir()


def test_deprecated(capsys):
    t_file, path = tempfile.mkstemp()
    os.close(t_file)
    assert write_yaml_file(path, {"foo": "bar"})
    out, err = capsys.readouterr()
    unlink_path(path)
    assert out.find(WRITE_YAML_DEPRECATED) != -1
