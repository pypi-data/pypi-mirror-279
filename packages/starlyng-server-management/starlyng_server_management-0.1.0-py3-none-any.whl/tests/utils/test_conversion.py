"""
Testing for conversion module
"""
import pytest
from server_management.utils.conversion import get_bcm_port, get_hostname

def test_get_bcm_port_local_ip():
    """
    Test that the function returns "623" for local IP addresses.
    """
    ip = "192.168.1.1"
    port = 2300
    expected_result = "623"
    assert get_bcm_port(ip, port) == expected_result

def test_get_bcm_port_public_ip_valid_port():
    """
    Test that the function returns the correct bcm_port for public IPs and valid ports.
    """
    ip = "203.0.113.1"
    port = 2250
    expected_result = "62350"
    assert get_bcm_port(ip, port) == expected_result

def test_get_bcm_port_public_ip_port_min_boundary():
    """
    Test that the function handles the minimum boundary value for ports correctly.
    """
    ip = "203.0.113.1"
    port = 2200
    expected_result = "62300"
    assert get_bcm_port(ip, port) == expected_result

def test_get_bcm_port_public_ip_port_max_boundary():
    """
    Test that the function handles the maximum boundary value for ports correctly.
    """
    ip = "203.0.113.1"
    port = 2299
    expected_result = "62399"
    assert get_bcm_port(ip, port) == expected_result

def test_get_bcm_port_invalid_port_too_low():
    """
    Test that the function raises a ValueError for ports below the valid range.
    """
    ip = "203.0.113.1"
    port = 2199
    with pytest.raises(ValueError, match="Port number must be between 2200 and 2299: port = 2199"):
        get_bcm_port(ip, port)

def test_get_bcm_port_invalid_port_too_high():
    """
    Test that the function raises a ValueError for ports above the valid range.
    """
    ip = "203.0.113.1"
    port = 2300
    with pytest.raises(ValueError, match="Port number must be between 2200 and 2299: port = 2300"):
        get_bcm_port(ip, port)

def test_get_bcm_port_edge_case_zero_port():
    """
    Test that the function raises a ValueError for a port number of zero.
    """
    ip = "203.0.113.1"
    port = 0
    with pytest.raises(ValueError, match="Port number must be between 2200 and 2299: port = 0"):
        get_bcm_port(ip, port)

def test_get_bcm_port_edge_case_negative_port():
    """
    Test that the function raises a ValueError for negative port numbers.
    """
    ip = "203.0.113.1"
    port = -1
    with pytest.raises(ValueError, match="Port number must be between 2200 and 2299: port = -1"):
        get_bcm_port(ip, port)

def test_get_bcm_port_empty_ip():
    """
    Test that the function handles an empty IP string correctly.
    """
    ip = ""
    port = 2200
    expected_result = "62300"
    assert get_bcm_port(ip, port) == expected_result

def test_get_bcm_port_non_standard_ip():
    """
    Test that the function handles non-standard IP addresses correctly.
    """
    ip = "10.0.0.1"
    port = 2250
    expected_result = "62350"
    assert get_bcm_port(ip, port) == expected_result

def test_get_hostname_private_ip():
    """
    Test hostnames for private ip addresses
    """
    assert get_hostname("192.168.10.10", 22) == "starlyng00"
    assert get_hostname("192.168.10.15", 22) == "starlyng05"
    assert get_hostname("192.168.10.30", 22) == "starlyng20"
    assert get_hostname("192.168.10.45", 22) == "starlyng35"

def test_get_hostname_public_ip():
    """
    Test hostnames for public ip addresses
    """
    assert get_hostname("10.0.0.1", 2200) == "starlyng00"
    assert get_hostname("172.16.0.1", 2290) == "starlyng90"

def test_get_hostname_invalid_port():
    """
    Test hostnames for invalid ports on public ip addresses
    """
    with pytest.raises(ValueError, match="Port number must be between 2200 and 2299: port = 2100"):
        get_hostname("10.0.0.1", 2100)
    with pytest.raises(ValueError, match="Port number must be between 2200 and 2299: port = 2400"):
        get_hostname("10.0.0.1", 2400)

def test_get_hostname_invalid_ip_base_address_range():
    """
    Test hostnames for invalid base ip address on private ip addresses
    """
    with pytest.raises(ValueError, match="IP base address must be between 10 and 255: ip_base_address = 9"):
        get_hostname("192.168.10.9", 22)  # This IP would create a ip_base_address of 9
    with pytest.raises(ValueError, match="IP base address must be between 10 and 255: ip_base_address = 256"):
        get_hostname("192.168.10.256", 22)  # This IP would create a ip_base_address of 256
