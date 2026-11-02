from dataclasses import dataclass
from typing import Any


@dataclass
class Memory:
    data: dict[str, Any]

    def __post_init__(self) -> None:
        if not isinstance(self.data, dict):
            raise TypeError

    def get(self) -> dict[str, Any]:
        return self.data
