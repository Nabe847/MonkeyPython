
ILLEGAL = "ILLEGAL"
EOF = "EOF"

# 識別子 + リテラル
IDENT = "IDENT"
INT = "INT"

# 演算子
ASSIGN = "="
PLUS = "+"

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


class Token:
    def __init__(self, token_type, literal):
        self.token_type = token_type
        self.literal = literal

    def __str__(self):
        return f'token_type: {self.token_type}, literal: {self.literal}'
