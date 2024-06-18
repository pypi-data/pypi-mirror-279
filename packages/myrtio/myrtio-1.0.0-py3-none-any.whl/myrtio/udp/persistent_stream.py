"""Persistent datagram stream"""
import logging
from typing import Optional

from asyncio_datagram import DatagramClient, TransportClosed, connect

Address = tuple[str, int]

class PersistentDatagramStream:
    """Persistent datagram stream"""
    _host_addr: Address
    _peer_addr: Optional[Address] = None
    _stream: Optional[DatagramClient] = None

    def __init__(self, addr: Address):
        self._host_addr = addr

    async def connect(self):
        """Connects to host"""
        logging.debug("PersistentDatagramStream: connecting to %s", self._host_addr)
        if self._stream is None:
            self._stream = await connect(
                self._host_addr,
                local_addr=self._peer_addr,
                reuse_port=True)
            if self._peer_addr is None:
                self._peer_addr = self._stream.sockname
        logging.debug("PersistentDatagramStream: connected to %s", self._host_addr)

    def close(self):
        """Closes stream"""
        logging.debug("PersistentDatagramStream: close")
        if self._stream is None:
            return
        self._stream.close()
        self._stream = None

    async def reconnect(self):
        """Reconnects to host"""
        if self.connected:
            self.close()
        await self.connect()

    @property
    def port(self) -> int:
        """Returns stream host port."""
        _, port = self._peer_addr
        return port

    @property
    def addr(self) -> Address:
        """Returns stream host address."""
        return self._host_addr

    @property
    def connected(self) -> bool:
        """Returns true if stream is connected"""
        return self._stream is not None

    async def read(self) -> Optional[list[int]]:
        """Reads message from stream"""
        if self._stream is None:
            return None
        try:
            data, _ = await self._stream.recv()
            logging.debug("PersistentDatagramStream: got data (%s)", list(data))
            return list(data)
        except (TransportClosed, RuntimeError):
            logging.debug("PersistentDatagramStream: error on read")
            self._stream = None
        return None

    async def send(self, payload: list[int]) -> bool:
        """Sends message to stream"""
        if self._stream is None:
            return False
        try:
            await self._stream.send(bytes(payload))
            logging.debug("PersistentDatagramStream: sended data %s", list(payload))
            return True
        except (TransportClosed, RuntimeError):
            logging.debug("PersistentDatagramStream: error on write")
            self._stream = None
        return False
