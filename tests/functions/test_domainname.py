"""Tests.functions.test_domainname module for wtforglib package."""

# mypy: disable_error_code = var-annotated

from pathlib import Path

import tomli

from wtforglib.constants import VERSION
from wtforglib.functions import domainname


def test_domainname():
    """Test domainname function."""
    assert domainname(True) == "example.com"
    assert domainname() == "example.com"


def test_version():
    """Test version function."""
    version: str
    with open(
        Path(__file__).parent.parent.parent.resolve() / "pyproject.toml", mode="rb"
    ) as pyproject:
        version = tomli.load(pyproject)["project"]["version"]
    assert VERSION == version
