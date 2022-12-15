from wtforglib import validators

# mypy: disable_error_code = var-annotated


def test_url_validator():
    """Test url_validator function."""
    assert not validators.url_validator("example.com")
    assert validators.url_validator("https://example.com/path")
    assert not validators.url_validator(532)  # type: ignore
