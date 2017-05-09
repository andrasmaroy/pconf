from ast import literal_eval
import json


# TODO: add docstring
class File():
    ENCODINGS = {
        'json': json.loads,
        'raw': literal_eval
    }

    def __init__(self, path, encoding='raw', parser=None):
        self.__open_file(path)
        self.__set_encoding(encoding, parser)

    def get(self):
        if self.file_handle is None or self.parser is None:
            return {}
        return self.parser(self.file_handle.read())

    def __open_file(self, path):
        try:
            self.file_handle = open(path, 'r')
        except IOError:
            # TODO: log warning here
            self.file_handle = None

    def __set_encoding(self, encoding, parser=None):
        try:
            self.parser = self.ENCODINGS[encoding]
        except KeyError:
            # TODO: log warning here
            self.parser = parser
