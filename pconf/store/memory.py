class Memory(object):
    def __init__(self, data):
        if type(data) != dict:
            raise TypeError
        self.data = data

    def get(self):
        return self.data
