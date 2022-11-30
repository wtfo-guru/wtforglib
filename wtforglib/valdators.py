from urllib.parse import urlparse


def url_validator(url: str) -> bool:
    """Validate url."""
    try:
        result = urlparse(url)
        print(result)
        return all([result.scheme, result.netloc, result.path])
    except ValueError:
        return False
