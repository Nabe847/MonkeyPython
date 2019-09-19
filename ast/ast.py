
class Node:
    def __init__(self, token):
        self.token

    def token_literal():
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
    def __init__(self, token):
        super().__init__(token)
        self.statements = []

    def token_literal(self):
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ''


class Identifier(Expression):
    def __init__(self, token):
        super().__init__(token)
        self.token = None
        self.value = None

    def __str__(self):
        return str(self.token)


class LetStatement(Statement):
    def __init__(self, token):
        super().__init__(token)
        self.token = None
        self.name = None
        self.value = None

    def token_literal(self):
        return str(self.token)
