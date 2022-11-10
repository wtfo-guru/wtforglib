from wtforglib.functions import hostname

# mypy: disable_error_code = var-annotated


def test_domainname():
    """Test hostname function."""
    assert hostname(True) == "nombre"
    assert hostname() == "nombre"
