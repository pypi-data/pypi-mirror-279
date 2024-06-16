from typing import Protocol, Literal, Iterator, Any

class CtrlMessage(Protocol):
    message_type: Literal['control']
    message_name: str
    message_id: int
    def unpack(self, data: bytes, we_are_a_client: bool = True) -> bool:
        ...
    def pack(self, we_are_a_client: bool = True) -> bytes:
        ...
    def __iter__(self) -> Iterator[tuple[str, Any]]:
        ...
