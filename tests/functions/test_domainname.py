from wtforglib.functions import domainname

# mypy: disable_error_code = var-annotated


def test_domainname():
    """Test domainname function."""
    assert domainname(True) == "example.com"
    assert domainname() == "example.com"
