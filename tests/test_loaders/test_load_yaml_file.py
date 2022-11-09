import tempfile
from pathlib import Path

import pytest

from wtforglib.loaders import load_yaml_file

LAYOUT = """---
foo: bar
...
"""


def test_load_yaml_file():
    """Test load_yaml_file function."""
    _t_file, path = tempfile.mkstemp()
    with open(path, mode="w") as yfile:
        yfile.write(LAYOUT)
        yfile.close()
    test_me = load_yaml_file(path)
    Path(path).unlink(missing_ok=True)
    assert isinstance(test_me, dict)
    assert test_me["foo"] == "bar"


def test_load_yaml_file_missing():
    """Test load_yaml_file function with missing_ok=False."""
    _t_file, path = tempfile.mkstemp()
    Path(path).unlink(missing_ok=True)
    missing_path = str(path) + ".missing"
    with pytest.raises(FileNotFoundError):
        load_yaml_file(missing_path, False)


def test_load_yaml_file_directroy():
    """Test load_yaml_file function passing a directory for file."""
    path = tempfile.mkdtemp()
    with pytest.raises(FileNotFoundError):
        load_yaml_file(path, False)
    Path(path).rmdir()
