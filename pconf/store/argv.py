import argparse
from ast import literal_eval


class Argv(object):
    parser = None

    def __init__(self, name, short_name=None, type=None, help=None):
        if Argv.parser is None:
            Argv.parser = argparse.ArgumentParser()

        self.results = {}

        args = {}
        args['help'] = help
        if type == bool:
            args['action'] = 'store_true'
        # types supported by literal_eval
        elif type in [dict, list, tuple]:
            args['type'] = literal_eval
        elif type == 'repeated_list':
            args['action'] = 'append'
        else:
            args['type'] = type

        if short_name is not None:
            Argv.parser.add_argument(name, short_name, default=argparse.SUPPRESS, **args)
        else:
            Argv.parser.add_argument(name, default=argparse.SUPPRESS, **args)

    def get(self):
        namespace, _ = Argv.parser.parse_known_args()
        self.results = vars(namespace)
        return self.results
