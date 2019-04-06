import monkey_token


class Lexer:
    def __init__(self, inputs):
        self.__inputs = inputs
        self.__position = -1  # 入力文字列における現在の位置
        self.__read_position = 0  # これから読み込む文字の位置
        self.__ch = '\0'  # 検査中の文字
        self.__read_char()

    def __read_char(self):
        if self.__read_position >= len(self.__inputs):
            self.__ch = '\0'
        else:
            self.__ch = self.__inputs[self.__read_position]

        self.__position = self.__read_position
        self.__read_position += 1

    def next_token(self):
        token_type = None
        ch = self.__ch
        if ch == '=':
            token_type = monkey_token.ASSIGN
        elif ch == ';':
            token_type = monkey_token.SEMICOLON
        elif ch == '(':
            token_type = monkey_token.LPAREN
        elif ch == ')':
            token_type = monkey_token.RPAREN
        elif ch == ',':
            token_type = monkey_token.COMMA
        elif ch == '+':
            token_type = monkey_token.PLUS
        elif ch == '{':
            token_type = monkey_token.LBRACE
        elif ch == '}':
            token_type = monkey_token.RBRACE
        elif ch == '\0':
            token_type = monkey_token.EOF
            ch == ""

        self.__read_char()

        tok = monkey_token.Token(token_type, ch)
        return tok
