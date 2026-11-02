from typing import Any


class Memory:
    def __init__(self, data: dict[str, Any]) -> None:
        if not isinstance(data, dict):
            raise TypeError
        self.data = data

    def get(self) -> dict[str, Any]:
        return self.data
