
INTEGER_OBJ = "INTEGER"
BOOLEAN_OBJ = "BOOLEAN"
NULL_OBJ = "NULL"
RETURN_VALUE_OBJ = "RETURN_VALUE"
ERROR_OBJ = "ERROR"
FUNCTION_OBJ = "FUNCTION"


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
        return str(self.value).lower()

    def type(self):
        return BOOLEAN_OBJ


class Null:
    def inspect(self):
        return "null"

    def type(self):
        return NULL_OBJ


class ReturnValue:
    def __init__(self, value):
        self.value = value

    def type(self):
        return RETURN_VALUE_OBJ

    def inspect(self):
        return self.value.inspect()


class Error:
    def __init__(self, message):
        self.message = message

    def type(self):
        return ERROR_OBJ

    def inspect(self):
        return "ERROR: " + self.message


class Function:
    def __init__(self, parameters, body, env):
        self.parameters = parameters
        self.body = body
        self.env = env

    def type(self):
        return FUNCTION_OBJ

    def inspect(self):
        s = "fn("
        s += ", ".join([str(p) for p in self.parameters])
        s += ") {\n"
        s += str(self.body)
        s += "\n}"
        return s
