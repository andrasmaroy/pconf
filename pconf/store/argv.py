import argparse
from ast import literal_eval
from typing import Any


class Argv:
    def __init__(
        self,
        name: str,
        short_name: str | None = None,
        type: type | str | None = None,
        help: str | None = None,
        parser: argparse.ArgumentParser | None = None,
    ) -> None:
        if not name.startswith("-") or name.count(" ") != 0:
            raise ValueError

        self.parser = parser if parser is not None else argparse.ArgumentParser()

        self.results: dict[str, Any] = {}

        args: dict[str, Any] = {}
        args["help"] = help
        if type is bool:
            args["action"] = "store_true"
        # types supported by literal_eval
        elif type in [dict, list, tuple]:
            args["type"] = literal_eval
        elif type == "repeated_list":
            args["action"] = "append"
        else:
            args["type"] = type

        if name.lstrip("-").count("-") != 0:
            args["dest"] = name.lstrip("-")

        if short_name is not None:
            self.parser.add_argument(name, short_name, default=argparse.SUPPRESS, **args)
        else:
            self.parser.add_argument(name, default=argparse.SUPPRESS, **args)

    def get(self) -> dict[str, Any]:
        namespace, _ = self.parser.parse_known_args()
        self.results = vars(namespace)
        return self.results
