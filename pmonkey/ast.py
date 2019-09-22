
class Node:
    def __init__(self, token):
        self.token = token

    def token_literal(self):
        return self.token.literal


class Statement(Node):
    def __init__(self, token):
        super().__init__(token)


class Expression(Node):
    def __init__(self, token):
        super().__init__(token)


class Program(Node):
    def __init__(self):
        super().__init__("")
        self.statements = []

    def token_literal(self):
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ""

    def __str__(self):
        return "\n".join([str(s) for s in self.statements])


class Identifier(Expression):
    def __init__(self, token):
        super().__init__(token)
        self.value = token.literal

    def __str__(self):
        return self.value


class IntegerLiteral(Expression):
    def __init__(self, token):
        super().__init__(token)
        self.value = None

    def __str__(self):
        return str(self.token_literal())


class PrefixExpression(Expression):
    def __init__(self, token):
        super().__init__(token)
        self.operator = self.token_literal()
        self.right = None

    def __str__(self):
        return f"({str(self.operator)}{self.right})"


class InfixExpression(Expression):
    def __init__(self, token):
        super().__init__(token)
        self.left = None
        self.operator = None
        self.right = None

    def __str__(self):
        s = "("
        s += str(self.left)
        s += self.operator
        s += str(self.right)
        s += ")"
        return s


class LetStatement(Statement):
    def __init__(self, token):
        super().__init__(token)
        self.name = None
        self.value = None

    def __str__(self):
        s = f"{self.token_literal()} {str(self.name)} = "
        if self.value:
            s += str(self.value)
        s += ";"
        return s


class ReturnStatement(Statement):
    def __init__(self, token):
        super().__init__(token)
        self.return_value = None

    def __str__(self):
        s = self.token_literal() + " "
        if self.return_value:
            s += str(self.return_value)
        s += ";"
        return s


class ExpressionStatement(Statement):
    def __init__(self, token):
        super().__init__(token)
        self.expression = None

    def __str__(self):
        if self.expression:
            return str(self.expression)
        else:
            return ""
