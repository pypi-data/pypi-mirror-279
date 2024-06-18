"""High-level UDP stream transport for MyrtIO devices"""
import asyncio
from typing import Optional

from ..message import Message, parse_message
from ..transport import MyrtIOTransport
from .persistent_stream import PersistentDatagramStream


class UDPTransport (MyrtIOTransport):
    """High-level UDP stream transport for MyrtDesk"""
    _stream: PersistentDatagramStream
    _timeout: int

    def __init__(self, host: str, port: int, timeout: int = 2):
        self._stream = PersistentDatagramStream((host, port))
        self._timeout = timeout

    async def connected(self) -> None:
        """Connects to host"""
        if not self._stream.connected:
            await self._stream.connect()

    async def run_action(self, message: Message) -> Optional[Message]:
        """Runs action"""
        try:
            async with asyncio.timeout(self._timeout):
                success = await self._stream.send(message.format_bytes())
                if not success:
                    return None
                resp = await self._stream.read()
                if resp is None:
                    return None
                return parse_message(resp)
        except asyncio.TimeoutError:
            await self._stream.reconnect()
            return None

    def close(self) -> None:
        """Closes stream"""
        self._stream.close()

async def connect_udp(host: str, port: int) -> MyrtIOTransport:
    """Creates UDP stream transport"""
    transport = UDPTransport(host, port)
    await transport.connected()
    return transport
