from typing import Protocol, Literal, Iterator, Any

from twnet_parser.chunk_header import ChunkHeader

class NetMessage(Protocol):
    message_type: Literal['system', 'game']
    message_name: str
    system_message: bool
    message_id: int
    header: ChunkHeader
    def unpack(self, data: bytes) -> bool:
        ...
    def pack(self) -> bytes:
        ...
    def __iter__(self) -> Iterator[tuple[str, Any]]:
        ...
