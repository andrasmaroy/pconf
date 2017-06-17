from ast import literal_eval
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
        'yaml': yaml.load
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
            self.content = ''

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
