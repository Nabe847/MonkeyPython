
class Node:
    def __init__(self, token):
        self.token = token

    def token_literal(self):
        return self.token.literal


class Statement(Node):
    def __init__(self, token):
        super().__init__(token)

    def statement_node(self):
        pass


class Expression(Node):
    def __init__(self, token):
        super().__init__(token)

    def expression_node(self):
        pass


class Program(Node):
    def __init__(self):
        super().__init__("")
        self.statements = []

    def token_literal(self):
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ""


class Identifier(Expression):
    def __init__(self, token):
        super().__init__(token)
        self.value = token.literal


class LetStatement(Statement):
    def __init__(self, token):
        super().__init__(token)
        self.name = None
        self.value = None
