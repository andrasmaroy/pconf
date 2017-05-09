import os


class Env(object):
    def __init__(self, separator=':', match=None, whitelist=None):
        self.separator = separator
        self.match = match
        self.whitelist = whitelist

    def get(self):
        env_vars = os.environ
        return env_vars
