import pmonkey.ast as ast
import pmonkey.token as token

LOWEST = 1
EQUALS = 2
LESSGREATER = 3
SUM = 4
PRODUCT = 5
PREFIX = 6
CALL = 7

PRECEDENCES = {
    token.EQ: EQUALS,
    token.NOT_EQ: EQUALS,
    token.LT: LESSGREATER,
    token.GT: LESSGREATER,
    token.PLUS: SUM,
    token.MINUS: SUM,
    token.SLASH: PRODUCT,
    token.ASTERISK: PRODUCT,
}

class Parser:
    def __init__(self, l):
        self.lexer = l
        self.cur_token = None
        self.peek_token = None
        self.next_token()
        self.next_token()
        self.program = ast.Program()
        self.errors = []

        self.prefix_parser_fns = {}
        self.infix_parser_fns = {}

        self.prefix_parser_fns[token.IDENT] = self.parse_identifier
        self.prefix_parser_fns[token.INT] = self.parse_integer_literal
        self.prefix_parser_fns[token.BANG] = self.parse_prefix_expression
        self.prefix_parser_fns[token.MINUS] = self.parse_prefix_expression
        self.prefix_parser_fns[token.TRUE] = self.parse_boolean_literal
        self.prefix_parser_fns[token.FALSE] = self.parse_boolean_literal
        self.prefix_parser_fns[token.LPAREN] = self.parse_grouped_expression
        self.prefix_parser_fns[token.IF] = self.parse_if_expression

        self.infix_parser_fns[token.PLUS] = self.parse_infix_expression
        self.infix_parser_fns[token.MINUS] = self.parse_infix_expression
        self.infix_parser_fns[token.SLASH] = self.parse_infix_expression
        self.infix_parser_fns[token.ASTERISK] = self.parse_infix_expression
        self.infix_parser_fns[token.EQ] = self.parse_infix_expression
        self.infix_parser_fns[token.NOT_EQ] = self.parse_infix_expression
        self.infix_parser_fns[token.LT] = self.parse_infix_expression
        self.infix_parser_fns[token.GT] = self.parse_infix_expression

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def cur_token_is(self, expected_type):
        return self.cur_token.token_type == expected_type

    def parse_program(self):
        self.program.statements = []
        self.errors = []
        while self.cur_token.token_type != token.EOF:
            statement = self.parse_statement()

            if statement != None:
                self.program.statements.append(statement)

            self.next_token()

        return self.program

    def parse_statement(self):
        if self.cur_token_is(token.LET):
            return self.parse_let_statement()
        elif self.cur_token_is(token.RETURN):
            return self.parse_return_statement()
        else:
            return self.parse_expression_statement()

    def parse_let_statement(self):

        let = ast.LetStatement(self.cur_token)

        if not self.expect_peek(token.IDENT):
            return None

        let.name = ast.Identifier(self.cur_token)

        if not self.expect_peek(token.ASSIGN):
            return None

        # TODO: 読み飛ばしている
        while not self.cur_token_is(token.SEMICOLON):
            self.next_token()

        return let

    def parse_return_statement(self):
        ret = ast.ReturnStatement(self.cur_token)

        self.next_token()

        # TODO: 読み飛ばしている
        while not self.cur_token_is(token.SEMICOLON):
            self.next_token()

        return ret
   
    def parse_expression_statement(self):
        statement = ast.ExpressionStatement(self.cur_token)
        statement.expression = self.parse_expression(LOWEST)

        if self.peek_token.token_type == token.SEMICOLON:
            self.next_token()

        return statement

    def parse_expression(self, precedence):
        if self.cur_token.token_type not in self.prefix_parser_fns:
            self.no_prefix_parse_fn_error(self.cur_token.token_type)
            return None

        prefix = self.prefix_parser_fns[self.cur_token.token_type]
        left_exp = prefix()

        while self.peek_token.token_type != token.SEMICOLON and precedence < self.peek_precedence():
            if self.peek_token.token_type not in self.infix_parser_fns:
                return left_exp

            infix = self.infix_parser_fns[self.peek_token.token_type]
            self.next_token()
            left_exp = infix(left_exp)

        return left_exp

    def parse_identifier(self):
        return ast.Identifier(self.cur_token)

    def parse_integer_literal(self):
        lit = ast.IntegerLiteral(self.cur_token)
        v = lit.token_literal()

        if not v.isdigit():
            self.errors.append(f"could not parse {v} as integer")
            return None

        lit.value = int(v)

        return lit
    
    def parse_boolean_literal(self):
        lit = ast.BooleanLiteral(self.cur_token)
        lit.value = self.cur_token.token_type == token.TRUE
        return lit

    def parse_prefix_expression(self):
        expression = ast.PrefixExpression(self.cur_token)
        self.next_token()
        expression.right = self.parse_expression(PREFIX)
        return expression
    
    def parse_infix_expression(self, left):
        precedence = self.cur_precedence()
        expression = ast.InfixExpression(self.cur_token)
        expression.left = left
        expression.operator = self.cur_token.literal
        self.next_token()
        expression.right = self.parse_expression(precedence)

        return expression

    def parse_grouped_expression(self):
        self.next_token()

        expression = self.parse_expression(LOWEST)

        if not self.expect_peek(token.RPAREN):
            return None
        
        return expression

    def parse_if_expression(self):
        expression = ast.IfExpression(self.cur_token)

        if not self.expect_peek(token.LPAREN):
            return None
        
        self.next_token()
        expression.condition = self.parse_expression(LOWEST)

        if not self.expect_peek(token.RPAREN):
            return None

        if not self.expect_peek(token.LBRACE):
            return None
        
        expression.consequence = self.parse_block_statement()

        return expression

    def parse_block_statement(self):
        block = ast.BlockStatement(self.cur_token)
        self.next_token()

        while self.cur_token.token_type != token.RBRACE \
            and self.cur_token.token_type != token.EOF:
            s = self.parse_statement()
            if s:
                block.statements.append(s)

            self.next_token()
        
        return block

    def expect_peek(self, expected_type):
        if self.peek_token.token_type == expected_type:
            self.next_token()
            return True
        else:
            self.peek_error(expected_type)
            return False

    def peek_precedence(self):
        if self.peek_token.token_type not in PRECEDENCES:
            return LOWEST
        
        return PRECEDENCES[self.peek_token.token_type]

    def cur_precedence(self):
        if self.cur_token.token_type not in PRECEDENCES:
            return LOWEST
        
        return PRECEDENCES[self.cur_token.token_type]

    def peek_error(self, expected_type):
        msg = f"expected next token to be {expected_type}, got {self.cur_token.token_type} insted"
        self.errors.append(msg)

    def no_prefix_parse_fn_error(self, token_type):
        self.errors.append(f"no prefix parse function for {token_type} found")
