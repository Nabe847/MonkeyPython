import unittest

import monkey_token
import lexer


class TestLexer(unittest.TestCase):
    def test_next_token(self):
        inputs = '=+(),;'
        tests = [
            monkey_token.Token(monkey_token.ASSIGN, "="),
            monkey_token.Token(monkey_token.PLUS, "+"),
            monkey_token.Token(monkey_token.LPAREN, "("),
            monkey_token.Token(monkey_token.RPAREN, ")"),
            monkey_token.Token(monkey_token.COMMA, ","),
            monkey_token.Token(monkey_token.SEMICOLON, ";"),
        ]

        lex = lexer.Lexer(inputs)

        for expected in tests:
            tok = lex.next_token()
            print(tok)
            self.assertEqual(tok.token_type, expected.token_type)
            self.assertEqual(tok.literal, expected.literal)


if __name__ == '__main__':
    unittest.main()
