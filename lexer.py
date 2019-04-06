import monkey_token


class Lexer:
    def __init__(self, inputs):
        self.__inputs = inputs
        self.__position = -1  # 入力文字列における現在の位置
        self.__read_position = 0  # これから読み込む文字の位置
        self.__ch = ''  # 検査中の文字
        self.__read_char()

    def __read_char(self):
        if self.__read_position >= len(self.__inputs):
            self.__ch = ''
        else:
            self.__ch = self.__inputs[self.__read_position]

        self.__position = self.__read_position
        self.__read_position += 1

    def __peekChar(self):
        if self.__read_position >= len(self.__inputs):
            return ''
        else:
            return self.__inputs[self.__read_position]

    def __read_identifier(self):
        position = self.__position
        while self.__is_letter(self.__ch):
            self.__read_char()

        return self.__inputs[position: self.__position]

    def __read_number(self):
        position = self.__position
        while self.__ch.isdigit():
            self.__read_char()

        return self.__inputs[position: self.__position]

    def __skip_whitespace(self):
        while self.__ch.isspace():
            self.__read_char()

    def __is_letter(self, ch):
        return ch.isalpha() or ch == '_'

    def next_token(self):
        self.__skip_whitespace()

        token_type = None
        ch = self.__ch
        if ch == '=':
            if self.__peekChar() == '=':
                self.__read_char()
                ch = ch + self.__ch
                token_type = monkey_token.EQ
            else:
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
        elif ch == '-':
            token_type = monkey_token.MINUS
        elif ch == '/':
            token_type = monkey_token.SLASH
        elif ch == '*':
            token_type = monkey_token.ASTERISK
        elif ch == '!':
            if self.__peekChar() == '=':
                self.__read_char()
                ch = ch + self.__ch
                token_type = monkey_token.NOT_EQ
            else:
                token_type = monkey_token.BANG
        elif ch == '<':
            token_type = monkey_token.LT
        elif ch == '>':
            token_type = monkey_token.GT
        elif ch == '{':
            token_type = monkey_token.LBRACE
        elif ch == '}':
            token_type = monkey_token.RBRACE
        elif ch == '':
            token_type = monkey_token.EOF
        else:
            if self.__is_letter(ch):
                literal = self.__read_identifier()
                token_type = monkey_token.lookup_ident(literal)
                tok = monkey_token.Token(token_type, literal)
                return tok
            elif ch.isdigit():
                literal = self.__read_number()
                token_type = monkey_token.INT
                tok = monkey_token.Token(token_type, literal)
                return tok
            else:
                token_type = monkey_token.ILLEGAL

        self.__read_char()

        tok = monkey_token.Token(token_type, ch)
        return tok
