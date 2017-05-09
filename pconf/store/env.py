import os


class Env(object):
    def __init__(self):
        pass

    def get(self):
        env_vars = os.environ
        return env_vars
