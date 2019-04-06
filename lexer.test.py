import unittest

import lexer
import monkey_token
from monkey_token import Token


class TestLexer(unittest.TestCase):
    def test_next_token(self):
        inputs = """let five = 5;
        let ten = 10;
        let add = fn(x, y) {
            x + y;
        }
        let result = add(five, ten);

        !-/*5;
        5 < 10 > 5;

        if (5 < 10) {
            return true;
        } else {
            return false;
        }

        10 == 10;
        10 != 9;

        """
        tests = [
            Token(monkey_token.LET, "let"),
            Token(monkey_token.IDENT, "five"),
            Token(monkey_token.ASSIGN, "="),
            Token(monkey_token.INT, "5"),
            Token(monkey_token.SEMICOLON, ";"),

            Token(monkey_token.LET, "let"),
            Token(monkey_token.IDENT, "ten"),
            Token(monkey_token.ASSIGN, "="),
            Token(monkey_token.INT, "10"),
            Token(monkey_token.SEMICOLON, ";"),

            Token(monkey_token.LET, "let"),
            Token(monkey_token.IDENT, "add"),
            Token(monkey_token.ASSIGN, "="),
            Token(monkey_token.FUNCTION, "fn"),
            Token(monkey_token.LPAREN, "("),
            Token(monkey_token.IDENT, "x"),
            Token(monkey_token.COMMA, ","),
            Token(monkey_token.IDENT, "y"),
            Token(monkey_token.RPAREN, ")"),
            Token(monkey_token.LBRACE, "{"),
            Token(monkey_token.IDENT, "x"),
            Token(monkey_token.PLUS, "+"),
            Token(monkey_token.IDENT, "y"),
            Token(monkey_token.SEMICOLON, ";"),
            Token(monkey_token.RBRACE, "}"),

            Token(monkey_token.LET, "let"),
            Token(monkey_token.IDENT, "result"),
            Token(monkey_token.ASSIGN, "="),
            Token(monkey_token.IDENT, "add"),
            Token(monkey_token.LPAREN, "("),
            Token(monkey_token.IDENT, "five"),
            Token(monkey_token.COMMA, ","),
            Token(monkey_token.IDENT, "ten"),
            Token(monkey_token.RPAREN, ")"),
            Token(monkey_token.SEMICOLON, ";"),

            Token(monkey_token.BANG, "!"),
            Token(monkey_token.MINUS, "-"),
            Token(monkey_token.SLASH, "/"),
            Token(monkey_token.ASTERISK, "*"),
            Token(monkey_token.INT, "5"),
            Token(monkey_token.SEMICOLON, ";"),
            Token(monkey_token.INT, "5"),
            Token(monkey_token.LT, "<"),
            Token(monkey_token.INT, "10"),
            Token(monkey_token.GT, ">"),
            Token(monkey_token.INT, "5"),
            Token(monkey_token.SEMICOLON, ";"),

            Token(monkey_token.IF, "if"),
            Token(monkey_token.LPAREN, "("),
            Token(monkey_token.INT, "5"),
            Token(monkey_token.LT, "<"),
            Token(monkey_token.INT, "10"),
            Token(monkey_token.RPAREN, ")"),

            Token(monkey_token.LBRACE, "{"),
            Token(monkey_token.RETURN, "return"),
            Token(monkey_token.TRUE, "true"),
            Token(monkey_token.SEMICOLON, ";"),
            Token(monkey_token.RBRACE, "}"),

            Token(monkey_token.ELSE, "else"),
            Token(monkey_token.LBRACE, "{"),
            Token(monkey_token.RETURN, "return"),
            Token(monkey_token.FALSE, "false"),
            Token(monkey_token.SEMICOLON, ";"),
            Token(monkey_token.RBRACE, "}"),

            Token(monkey_token.INT, "10"),
            Token(monkey_token.EQ, "=="),
            Token(monkey_token.INT, "10"),
            Token(monkey_token.SEMICOLON, ";"),

            Token(monkey_token.INT, "10"),
            Token(monkey_token.NOT_EQ, "!="),
            Token(monkey_token.INT, "9"),
            Token(monkey_token.SEMICOLON, ";"),

            Token(monkey_token.EOF, ""),
        ]

        lex = lexer.Lexer(inputs)

        for expected in tests:
            tok = lex.next_token()
            print(tok)
            self.assertEqual(tok.token_type, expected.token_type)
            self.assertEqual(tok.literal, expected.literal)


if __name__ == '__main__':
    unittest.main()
