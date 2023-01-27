"""Test module for wtforglib package."""
import platform
import pytest
from wtforglib.supers import issuper, requires_super_user

WINDOZE = "Windows"

if platform.system() == WINDOZE:
    pytest.skip("skipping tests on windows platform", allow_module_level=True)

def test_issuper():
    """Test issuper function."""
    assert not issuper()


def test_requires_super_user():
    """Test requires_super_user function."""
    with pytest.raises(PermissionError):
        requires_super_user()
