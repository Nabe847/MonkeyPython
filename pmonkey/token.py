
ILLEGAL = "ILLEGAL"
EOF = "EOF"

# 識別子 + リテラル
IDENT = "IDENT"
INT = "INT"

# 演算子
ASSIGN = "="
PLUS = "+"
MINUS = "-"
BANG = "!"
ASTERISK = "*"
SLASH = "/"

LT = "<"
GT = ">"
EQ = "=="
NOT_EQ = "!="

# デリミタ
COMMA = ","
SEMICOLON = ";"

LPAREN = "("
RPAREN = ")"
LBRACE = "{"
RBRACE = "}"

# キーワード
FUNCTION = "FUNCTION"
LET = "LET"
TRUE = "TRUE"
FALSE = "FALSE"
IF = "IF"
ELSE = "ELSE"
RETURN = "RETURN"

keywords = {
    "fn": FUNCTION,
    "let": LET,
    "true": TRUE,
    "false": FALSE,
    "if": IF,
    "else": ELSE,
    "return": RETURN,
}


def lookup_ident(ident):
    return keywords.get(ident, IDENT)


class Token:
    def __init__(self, token_type, literal):
        self.token_type = token_type
        self.literal = literal

    def __str__(self):
        return f'[token_type: {self.token_type: <10}][literal: {self.literal: <10}]'
