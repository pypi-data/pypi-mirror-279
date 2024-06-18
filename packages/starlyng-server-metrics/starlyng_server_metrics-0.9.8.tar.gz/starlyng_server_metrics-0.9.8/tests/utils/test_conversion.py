"""
Testing for conversion module
"""
import pytest
from server_metrics.utils.conversion import (
    convert_frequency_to_number,
    convert_lanes_to_number,
    convert_memory_to_number,
    convert_percentage_to_number,
    convert_power_to_number,
    convert_temperature_to_number,
    convert_voltage_to_number,
    get_hostname
)

def test_convert_frequency_to_number():
    """
    Tests converting MHz to number
    """
    assert convert_frequency_to_number("300 MHz") == 300
    assert convert_frequency_to_number("  5000   MHz  ") == 5000
    with pytest.raises(ValueError):
        convert_frequency_to_number("invalid")

def test_convert_lanes_to_number():
    """
    Tests converting 16x to number
    """
    assert convert_lanes_to_number("16x") == 16
    assert convert_lanes_to_number("  8   x  ") == 8
    with pytest.raises(ValueError):
        convert_lanes_to_number("invalid")

def test_convert_memory_to_number():
    """
    Tests converting MiB to number
    """
    assert convert_memory_to_number("24576 MiB") == 24576
    assert convert_memory_to_number("  1024   MiB  ") == 1024
    with pytest.raises(ValueError):
        convert_memory_to_number("invalid")

def test_convert_percentage_to_number():
    """
    Tests converting percentage to number
    """
    assert convert_percentage_to_number("0 %") == 0
    assert convert_percentage_to_number("  75   %  ") == 75
    with pytest.raises(ValueError):
        convert_percentage_to_number("invalid")

def test_convert_power_to_number():
    """
    Tests converting W (watts) to number
    """
    assert convert_power_to_number("42.65 W") == 42.65
    assert convert_power_to_number("  100.5   W  ") == 100.5
    with pytest.raises(ValueError):
        convert_power_to_number("invalid")

def test_convert_temperature_to_number():
    """
    Tests converting C (celcius) to number
    """
    assert convert_temperature_to_number("41 C") == 41
    assert convert_temperature_to_number("  100   C  ") == 100
    with pytest.raises(ValueError):
        convert_temperature_to_number("invalid")

def test_convert_voltage_to_number():
    """
    Tests converting mV (voltage) to number
    """
    assert convert_voltage_to_number("737.500 mV") == 737.5
    assert convert_voltage_to_number("  1000.0   mV  ") == 1000.0
    with pytest.raises(ValueError):
        convert_voltage_to_number("invalid")

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
