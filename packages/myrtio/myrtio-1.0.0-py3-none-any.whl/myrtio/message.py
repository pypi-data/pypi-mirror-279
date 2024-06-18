from .bytes import assert_byte
from .constants import (
    FIRST_HEADER_CODE,
    MAX_PAYLOAD_LENGTH,
    MIN_MESSAGE_LENGTH,
    SECOND_HEADER_CODE,
    SUCCESS_CODE,
    TAIL_CODE,
)


class Message:
    _feature: int
    _action: int
    _payload: bytes

    def __init__(self, feature: int, action: int, payload: bytes = None):
        assert_byte(feature)
        assert_byte(action)
        if payload is not None and len(payload) > MAX_PAYLOAD_LENGTH:
            raise ValueError("Payload is too long")
        self._feature = feature
        self._action = action
        if payload is None:
            payload = []
        self._payload = bytes(payload)

    def format_bytes(self) -> bytes:
        """Formats message bytes"""
        return bytes([
            FIRST_HEADER_CODE,
            SECOND_HEADER_CODE,
            len(self._payload)+2,
            self._feature,
            self._action,
            *self._payload,
            TAIL_CODE
        ])

    @property
    def feature(self) -> int:
        """Message feature code"""
        return self._feature

    @property
    def action(self) -> int:
        """Message action code"""
        return self._action

    @property
    def payload(self) -> bytes:
        """Message payload"""
        return self._payload

    @property
    def payload_without_status(self) -> bytes:
        return self._payload[1:]

    @property
    def is_successful(self) -> bool:
        """Is message successful"""
        return len(self._payload) > 0 and self._payload[0] == SUCCESS_CODE

def parse_message(message: bytes) -> Message:
    """Parse message from bytes"""
    if len(message) < 6:
        raise ValueError("Not enough bytes to parse message")
    if message[0] != FIRST_HEADER_CODE or message[1] != SECOND_HEADER_CODE:
        raise ValueError("Invalid header")
    payload_length = message[2] - 2
    if len(message) != MIN_MESSAGE_LENGTH + payload_length:
        raise ValueError("Not enough bytes to parse message")
    return Message(
        feature=message[3],
        action=message[4],
        payload=message[5:5+payload_length],
    )
