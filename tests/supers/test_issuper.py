from wtforglib.supers import issuper

# mypy: disable_error_code = var-annotated


def test_issuper():
    """Test issuper function."""
    assert not issuper()
