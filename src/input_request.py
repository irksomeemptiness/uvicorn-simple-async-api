import json
from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass(repr=True)
class InputRequest:
    type: str
    asgi: dict
    http_version: str
    server: tuple[str, int]
    client: tuple[str, int]
    scheme: str
    method: str
    root_path: str
    path: str
    raw_path: str
    query_string: bytes
    headers: list[tuple[bytes, bytes]]
    state: str
    _body: Optional[Any] = field(default_factory=str)

    @property
    def body(self) -> dict:
        return json.loads(self._body.decode())

    @property
    def params(self) -> list:
        params: list[dict] = []
        if not self.query_string:
            return params

        for batch in self.query_string.decode().split('&'):
            key, value = batch.split('=')
            params.append({key: value})
        return params
