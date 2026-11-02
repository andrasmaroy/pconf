from ast import literal_eval
from configparser import ConfigParser
from typing import Any, Callable
from warnings import warn
import json
import yaml


def parse_ini(content: str) -> dict[str, Any]:
    config = ConfigParser(allow_no_value=True)
    config.read_string(content)
    if len(config.sections()) == 0:
        return dict(config.items("DEFAULT"))
    result = {}
    for section in config.sections():
        result[section] = dict(config.items(section))
    return result


class File:
    ENCODINGS: dict[str, Callable[[str], Any]] = {
        "ini": parse_ini,
        "json": json.loads,
        "raw": literal_eval,
        "yaml": yaml.safe_load,
    }

    def __init__(self, path: str, encoding: str | None = "raw", parser: Callable[[str], Any] | None = None) -> None:
        self.content: Any = None
        self.__read_file(path)
        self.__set_encoding(encoding, parser)
        self.__parse_content()
        self.__clear_empty_values()

    def get(self) -> dict[str, Any]:
        return self.content

    def __read_file(self, path: str) -> None:
        try:
            with open(path, "r") as f:
                self.content = f.read()
        except OSError:
            warn(f"IOError when opening {path}", UserWarning)
            self.content = {}

    def __set_encoding(self, encoding: str | None, parser: Callable[[str], Any] | None = None) -> None:
        self.parser: Callable[[str], Any] | None = self.ENCODINGS.get(encoding, parser) if encoding is not None else parser

    def __parse_content(self) -> None:
        try:
            self.content = self.parser(self.content)  # type: ignore[misc]
            if not isinstance(self.content, dict):
                self.content = {}
        except Exception as e:
            warn(f"Error parsing file contents: {e}", UserWarning)
            self.content = {}

    def __clear_empty_values(self) -> None:
        if not self.content:
            return
        self.content = {key: value for key, value in self.content.items() if value is not None}
