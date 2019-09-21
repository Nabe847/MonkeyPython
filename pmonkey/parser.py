import pmonkey.ast as ast
import pmonkey.token as token

class Parser:
    def __init__(self, l):
        self.lexer = l
        self.cur_token = None
        self.peek_token = None
        self.next_token()
        self.next_token()
        self.program = ast.Program()

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self):
        self.program.statements = []
        while self.cur_token.token_type != token.EOF:
            statement = self.parse_statement()

            if statement != None:
                self.program.statements.append(statement)
            
            self.next_token()
        
        return self.program

    def parse_statement(self):
        if self.cur_token.token_type == token.LET:
            return self.parse_let_statement()
        else:
            return None
    
    def parse_let_statement(self):

        let = ast.LetStatement(self.cur_token)

        if not self.expect_peek(token.IDENT):
            return None
        
        let.name = ast.Identifier(self.cur_token)

        if not self.expect_peek(token.ASSIGN):
            return None

        # TODO: 読み飛ばしている
        while self.cur_token.token_type != token.SEMICOLON:
            self.next_token()
        
        return let
    
    def expect_peek(self, expect_type):
        if self.peek_token.token_type == expect_type:
            self.next_token()
            return True
        else:
            return False
