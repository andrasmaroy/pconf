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
        keys_to_delete = []
        dict_to_add = {}
        for key in env_vars.keys():
            splits = key.split(self.separator)
            splits = list(filter(None, splits))

            if len(splits) != 1:
                split = self.__split_var(splits, env_vars[key])
                keys_to_delete.append(key)
                self.__merge_split(split, dict_to_add)

        for key in keys_to_delete:
            del env_vars[key]
        env_vars.update(dict_to_add)

    def __split_var(self, keys, value):
        if len(keys) == 1:
            return {keys[0]: value}
        else:
            key = keys[0]
            del keys[0]
            return {key: self.__split_var(keys, value)}

    def __merge_split(self, split, env_vars):
        key = list(split.keys())[0]
        value = list(split.values())[0]
        if key not in env_vars:
            env_vars[key] = value
            return
        elif type(value) == dict:
            self.__merge_split(value, env_vars[key])
        else:
            return

    def __gather_vars(self):
        self.vars = {}
        env_vars = os.environ

        for key in env_vars.keys():
            if self.__valid_key(key):
                self.vars[key] = env_vars[key]

        if self.separator is not None:
            self.__split_vars(self.vars)
