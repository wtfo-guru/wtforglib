import pytest

from wtforglib.supers import requires_super_user

# mypy: disable_error_code = var-annotated


def test_requires_super_user():
    """Test requires_super_user function."""
    with pytest.raises(PermissionError):
        requires_super_user()
