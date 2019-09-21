import unittest

from pmonkey.lexer import Lexer
from pmonkey.token import Token
import pmonkey.token as token

# python -m unittest tests.test_lexer
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
            Token(token.LET, "let"),
            Token(token.IDENT, "five"),
            Token(token.ASSIGN, "="),
            Token(token.INT, "5"),
            Token(token.SEMICOLON, ";"),
            Token(token.LET, "let"),
            Token(token.IDENT, "ten"),
            Token(token.ASSIGN, "="),
            Token(token.INT, "10"),
            Token(token.SEMICOLON, ";"),
            Token(token.LET, "let"),
            Token(token.IDENT, "add"),
            Token(token.ASSIGN, "="),
            Token(token.FUNCTION, "fn"),
            Token(token.LPAREN, "("),
            Token(token.IDENT, "x"),
            Token(token.COMMA, ","),
            Token(token.IDENT, "y"),
            Token(token.RPAREN, ")"),
            Token(token.LBRACE, "{"),
            Token(token.IDENT, "x"),
            Token(token.PLUS, "+"),
            Token(token.IDENT, "y"),
            Token(token.SEMICOLON, ";"),
            Token(token.RBRACE, "}"),

            Token(token.LET, "let"),
            Token(token.IDENT, "result"),
            Token(token.ASSIGN, "="),
            Token(token.IDENT, "add"),
            Token(token.LPAREN, "("),
            Token(token.IDENT, "five"),
            Token(token.COMMA, ","),
            Token(token.IDENT, "ten"),
            Token(token.RPAREN, ")"),
            Token(token.SEMICOLON, ";"),

            Token(token.BANG, "!"),
            Token(token.MINUS, "-"),
            Token(token.SLASH, "/"),
            Token(token.ASTERISK, "*"),
            Token(token.INT, "5"),
            Token(token.SEMICOLON, ";"),
            Token(token.INT, "5"),
            Token(token.LT, "<"),
            Token(token.INT, "10"),
            Token(token.GT, ">"),
            Token(token.INT, "5"),
            Token(token.SEMICOLON, ";"),

            Token(token.IF, "if"),
            Token(token.LPAREN, "("),
            Token(token.INT, "5"),
            Token(token.LT, "<"),
            Token(token.INT, "10"),
            Token(token.RPAREN, ")"),

            Token(token.LBRACE, "{"),
            Token(token.RETURN, "return"),
            Token(token.TRUE, "true"),
            Token(token.SEMICOLON, ";"),
            Token(token.RBRACE, "}"),

            Token(token.ELSE, "else"),
            Token(token.LBRACE, "{"),
            Token(token.RETURN, "return"),
            Token(token.FALSE, "false"),
            Token(token.SEMICOLON, ";"),
            Token(token.RBRACE, "}"),

            Token(token.INT, "10"),
            Token(token.EQ, "=="),
            Token(token.INT, "10"),
            Token(token.SEMICOLON, ";"),

            Token(token.INT, "10"),
            Token(token.NOT_EQ, "!="),
            Token(token.INT, "9"),
            Token(token.SEMICOLON, ";"),

            Token(token.EOF, ""),
        ]

        lex = Lexer(inputs)

        for expected in tests:
            tok = lex.next_token()
            print(tok)
            self.assertEqual(tok.token_type, expected.token_type)
            self.assertEqual(tok.literal, expected.literal)


if __name__ == '__main__':
    unittest.main()
