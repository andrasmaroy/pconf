import os
import re


class Env(object):
    def __init__(self, separator=None, match=None, whitelist=None):
        self.separator = separator
        self.match = match
        self.whitelist = whitelist

        if self.match is not None:
            self.re = re.compile(self.match)

        self.__gather_vars()

    def get(self):
        return self.vars

    def __valid_key(self, key):
        if self.match is not None and self.whitelist is not None:
            return key in self.whitelist or self.re.search(key) is not None
        elif self.match is not None:
            return self.re.search(key) is not None
        elif self.whitelist is not None:
            return key in self.whitelist
        else:
            return True

    def __split_vars(self, env_vars):
        for key in env_vars.keys():
            splits = key.split(self.separator)
            splits = filter(None, splits)

            if len(splits) != 1:
                split = self.__split_var(splits, env_vars[key])
                del env_vars[key]
                env_vars[split.keys()[0]] = split.values()[0]

    def __split_var(self, keys, value):
        if len(keys) == 1:
            return {keys[0]: value}
        else:
            key = keys[0]
            del keys[0]
            return {key: self.__split_var(keys, value)}

    def __gather_vars(self):
        self.vars = {}
        env_vars = os.environ

        for key in env_vars.keys():
            if self.__valid_key(key):
                self.vars[key] = env_vars[key]

        if self.separator is not None:
            self.__split_vars(self.vars)
