import argparse
from ast import literal_eval


class Argv:
    def __init__(self, name, short_name=None, type=None, help=None, parser=None):
        if not name.startswith("-") or name.count(" ") != 0:
            raise ValueError

        self.parser = parser if parser is not None else argparse.ArgumentParser()

        self.results = {}

        args = {}
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

    def get(self):
        namespace, _ = self.parser.parse_known_args()
        self.results = vars(namespace)
        return self.results
