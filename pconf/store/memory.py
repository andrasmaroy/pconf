class Memory:
    def __init__(self, data):
        if not isinstance(data, dict):
            raise TypeError
        self.data = data

    def get(self):
        return self.data
