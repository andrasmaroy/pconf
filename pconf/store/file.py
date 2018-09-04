from ast import literal_eval
from six import iteritems
from warnings import warn
import json
import yaml

from sys import version_info
if (version_info.major < 3):
    import ConfigParser
    from StringIO import StringIO
else:
    import configparser as ConfigParser
    from io import StringIO


def parse_ini(content):
    config = ConfigParser.ConfigParser(allow_no_value=True)
    config.readfp(StringIO(content))
    if len(config.sections()) == 0:
        return dict(config.items('DEFAULT'))
    result = {}
    for section in config.sections():
        result[section] = dict(config.items(section))
    return result


class File():
    ENCODINGS = {
        'ini': parse_ini,
        'json': json.loads,
        'raw': literal_eval,
        'yaml': yaml.safe_load
    }

    def __init__(self, path, encoding='raw', parser=None):
        self.__read_file(path)
        self.__set_encoding(encoding, parser)
        self.__parse_content()
        self.__clear_empty_values()

    def get(self):
        return self.content

    def __read_file(self, path):
        try:
            with open(path, 'r') as f:
                self.content = f.read()
        except IOError:
            warn('IOError when opening {}'.format(path), UserWarning)
            self.content = {}

    def __set_encoding(self, encoding, parser=None):
        try:
            self.parser = self.ENCODINGS[encoding]
        except KeyError:
            self.parser = parser

    def __parse_content(self):
        try:
            self.content = self.parser(self.content)
        except:
            self.content = {}

    def __clear_empty_values(self):
        if not self.content:
            return
        keys_to_clear = []
        for key, value in iteritems(self.content):
            if value is None:
                keys_to_clear.append(key)
        for key in keys_to_clear:
            self.content.pop(key, None)
