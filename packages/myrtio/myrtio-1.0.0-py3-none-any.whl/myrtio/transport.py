"""MyrtIO transport interface"""
from .message import Message


class MyrtIOTransport:
    """MyrtIO transport interface"""

    async def run_action(self, message: Message) -> Message:
        """Runs action"""
        raise NotImplementedError()

    def close(self) -> None:
        """Closes transport"""
        raise NotImplementedError()
