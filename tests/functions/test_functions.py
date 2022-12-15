from wtforglib import functions

# mypy: disable_error_code = var-annotated


def test_strtobool():
    """Test strtobool function."""
    for st in ("true", "1", "t", "y", "yes"):
        assert functions.strtobool(st)
    for sf in ("false", "0", "2", "f", "n", "no"):
        assert not functions.strtobool(sf)
