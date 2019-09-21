import ast


class Parser:
    def __init__(self, l):
        self.lexer = l
        self.cur_token = None
        self.peek_token = None
        self.next_token()
        self.next_token()

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self):
        pass
