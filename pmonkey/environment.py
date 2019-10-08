
class Environment:
    def __init__(self):
        self.__store = {}

    def set(self, name, obj):
        self.__store[name] = obj

    def get(self, name):
        if name not in self.__store:
            return None

        return self.__store[name]

