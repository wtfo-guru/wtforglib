"""Test module for wtforglib package."""
import os
import tempfile
from pathlib import Path

import pytest

from wtforglib.files import load_yaml_file
from wtforglib.versioned import unlink_path

# mypy: disable_error_code = var-annotated

LAYOUT = """---
foo: bar
...
"""


def test_load_yaml_file():
    """Test load_yaml_file function."""
    t_file, path = tempfile.mkstemp()
    os.close(t_file)
    with open(path, mode="w") as yfile:
        yfile.write(LAYOUT)
        yfile.close()
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
