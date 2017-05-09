from ast import literal_eval


# TODO: add docstring
class File():
    ENCODINGS = {
        'raw': literal_eval
    }

    def __init__(self, path):
        self.__open_file(path)
        self.parser = literal_eval

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
