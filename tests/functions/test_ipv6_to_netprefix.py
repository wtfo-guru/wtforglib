import pytest

from wtforglib.ipaddress_foos import ipv6_to_netprefix


def test_valid_params():
    """Test valid parameters."""
    ipv6 = "1111:2222:3333:4444:5555:6666:7777:8888"
    width = 5
    increment = 5
    max_prefix = 128
    for prefix_len in (16, 32, 48, 64, 80, 96, 112, 128):
        test_net = ipv6_to_netprefix(ipv6, prefix_len)
        if prefix_len == max_prefix:
            assert test_net == "{0}/{1}".format(ipv6, prefix_len)
        else:
            assert test_net == "{0}:/{1}".format(ipv6[:width], prefix_len)
        width += increment


def test_invalid_address():
    """Test invalid ipv6 address."""
    ipv6 = "8.8.8.8"
    with pytest.raises(Exception) as exc_info:
        ipv6_to_netprefix(ipv6, 64)
    assert str(exc_info.value) == "Invalid ipv6 address: 8.8.8.8"


def test_invalid_prefix_len():
    """Test invalid prefix length."""
    ipv6 = "1111:2222:3333:4444:5555:6666:7777:8888"
    evalue = "Invalid prefix length: 56. Expected one of 16,32,48,64,80,96,112,128"
    with pytest.raises(ValueError) as exc_info:
        ipv6_to_netprefix(ipv6, 56)
    assert str(exc_info.value) == evalue
