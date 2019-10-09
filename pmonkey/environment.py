
class Environment:
    def __init__(self, outer=None):
        self.__outer = outer
        self.__store = {}

    def set(self, name, obj):
        self.__store[name] = obj

    def get(self, name):
        if name not in self.__store:
            if self.__outer != None:
                return self.__outer.get(name)
            else:
                return None

        return self.__store[name]
