import pytest

from wtforglib.ipaddress_foos import (
    ipv6_to_netprefix,
    is_ipv6,
    is_ipv6_address,
    is_ipv6_network,
)

IPV6_ADDRESS = "1111:2222:3333:4444:5555:6666:7777:8888"
IPV6_NETWORK = "1111:2222:3333:4444::/64"
IPV4_ADDRESS = "8.8.8.8"
INVALID_IP_ADDRESS = "INVALID_IP_ADDRESS"


def test_is_ipv6():
    """Test is ipv6."""
    assert is_ipv6(IPV6_ADDRESS)
    assert is_ipv6(IPV6_NETWORK)
    assert not is_ipv6(IPV4_ADDRESS)
    assert not is_ipv6(INVALID_IP_ADDRESS)


def test_is_ipv6_address():
    """Test is is_ipv6_address."""
    assert is_ipv6_address(IPV6_ADDRESS)
    assert not is_ipv6_address(IPV6_NETWORK)
    assert not is_ipv6_address(IPV4_ADDRESS)
    assert not is_ipv6_address(INVALID_IP_ADDRESS)


def test_is_ipv6_network():
    """Test is ipv6."""
    assert is_ipv6_network(IPV6_ADDRESS)
    assert is_ipv6_network(IPV6_NETWORK)
    assert not is_ipv6_network(IPV4_ADDRESS)
    assert not is_ipv6_network(INVALID_IP_ADDRESS)


def test_ipv6_to_netprefix_valid_params():
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


def test_ipv6_to_netprefix_postfix_valid_params():
    """Test valid parameters."""
    ipv6 = "1111:2222:3333:4444:5555:6666:7777:8888"
    width = 5
    increment = 5
    max_prefix = 128
    for prefix_len in (16, 32, 48, 64, 80, 96, 112, 128):
        test_net = ipv6_to_netprefix(ipv6, prefix_len, "postfix")
        if prefix_len == max_prefix:
            assert test_net == "[{0}]/{1}".format(ipv6, prefix_len)
        else:
            assert test_net == "[{0}:]/{1}".format(ipv6[:width], prefix_len)
        width += increment


def test_ipv6_to_netprefix_invalid_address():
    """Test invalid ipv6 address."""
    with pytest.raises(Exception) as exc_info:
        ipv6_to_netprefix(IPV4_ADDRESS, 64)
    assert str(exc_info.value) == "Invalid ipv6 address: {0}".format(IPV4_ADDRESS)


def test_ipv6_to_netprefix_invalid_prefix_len():
    """Test invalid prefix length."""
    evalue = "Invalid prefix length: 56. Expected one of 16,32,48,64,80,96,112,128"
    with pytest.raises(ValueError) as exc_info:
        ipv6_to_netprefix(IPV6_ADDRESS, 56)
    assert str(exc_info.value) == evalue
