class Pconf():
    def __init__(self, argv=None, env=None, file=None, defaults=None, overrides=None):
        self.argv = argv
        self.env = env
        self.file = file
        self.defaults = defaults
        self.overrides = overrides
