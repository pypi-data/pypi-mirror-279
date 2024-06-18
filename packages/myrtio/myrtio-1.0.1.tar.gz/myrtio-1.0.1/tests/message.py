"""MyrtIO message tests"""

from myrtio import Message, parse_message
from myrtio.constants import (
    ERROR_CODE,
    FIRST_HEADER_CODE,
    SECOND_HEADER_CODE,
    SUCCESS_CODE,
    TAIL_CODE,
)


def test_message_bytes():
    """Test message to bytes conversion"""
    feature_code = 1
    action_code = 2
    payload = [3, 4, 5]

    msg = Message(
        feature=feature_code,
        action=action_code,
        payload=payload,
    )

    assert msg.format_bytes() == bytes([
        FIRST_HEADER_CODE,
        SECOND_HEADER_CODE,
        len(payload)+2,
        feature_code,
        action_code,
        payload[0],
        payload[1],
        payload[2],
        TAIL_CODE
    ])

def test_parse_message():
    """Test message parsing"""
    msg = parse_message([
        FIRST_HEADER_CODE,
        SECOND_HEADER_CODE,
        5,
        1,
        2,
        3,
        4,
        5,
        TAIL_CODE
    ])

    assert msg.feature == 1
    assert msg.action == 2
    assert msg.payload == bytes([3, 4, 5])

def test_status():
    """Test message status"""
    msg = parse_message([
        FIRST_HEADER_CODE,
        SECOND_HEADER_CODE,
        3,
        0,
        0,
        SUCCESS_CODE,
        TAIL_CODE
    ])
    assert msg.is_successful

    msg = parse_message([
        FIRST_HEADER_CODE,
        SECOND_HEADER_CODE,
        3,
        0,
        0,
        ERROR_CODE,
        TAIL_CODE
    ])
    assert not msg.is_successful

