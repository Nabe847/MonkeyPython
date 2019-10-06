
INTEGER_OBJ = "INTEGER"
BOOLEAN_OBJ = "BOOLEAN"
NULL_OBJ = "NULL"

class Integer:
    def __init__(self, value):
        self.value = value
    
    def inspect(self):
        return str(self.value)
    
    def type(self):
        return INTEGER_OBJ

class Boolean:
    def __init__(self, value):
        self.value = value

    def inspect(self):
        return str(self.value)
    
    def type(self):
        return BOOLEAN_OBJ

class Null:
    def inspect(self):
        return "null"
    
    def type(self):
        return NULL_OBJ
