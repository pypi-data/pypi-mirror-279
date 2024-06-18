"""MyrtIO byte utils"""

def split_byte_pair(value: int) -> tuple[int, int]:
    """Splits number into high and low bytes"""
    return value >> 8, value & 0xff

def from_byte_pair(high: int, low: int) -> int:
    """Assembles a number from high and low bytes."""
    return (high << 8) + low

def assert_byte(value: int):
    """Asserts that number is in range from 0 to 255"""
    assert 0 <= value <= 255
