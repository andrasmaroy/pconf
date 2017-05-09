from ast import literal_eval
import json


# TODO: add docstring
class File():
    ENCODINGS = {
        'json': json.loads,
        'raw': literal_eval
    }

    def __init__(self, path, encoding='raw', parser=None):
        self.__read_file(path)
        self.__set_encoding(encoding, parser)
        self.__parse_content()

    def get(self):
        return self.content

    def __read_file(self, path):
        try:
            with open(path, 'r') as f:
                self.content = f.read()
        except IOError:
            # TODO: log warning here
            self.content = ''

    def __set_encoding(self, encoding, parser=None):
        try:
            self.parser = self.ENCODINGS[encoding]
        except KeyError:
            # TODO: log warning here
            self.parser = parser

    def __parse_content(self):
        try:
            self.content = self.parser(self.content)
        except:
            # TODO: log warning here
            self.content = {}
