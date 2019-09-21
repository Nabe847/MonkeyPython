import unittest
from pmonkey.lexer import Lexer
from pmonkey.parser import Parser
from pmonkey import ast


# python -m unittest tests.test_ast
class TestParser(unittest.TestCase):
    def test_let_statements(self):
        input = """
        let x = 5;
        let y = 10;
        let foobar = 838383;
        """
        l = Lexer(input)
        program = Parser(l).parse_program()

        self.assertIsNotNone(program)
        self.assertEqual(3, len(program.statements))

        tests = ["x", "y", "foobar"]

        for test, statement in zip(tests, program.statements):
            self.assert_valid_let_statement(test, statement)

    def assert_valid_let_statement(self, name, statement):
        self.assertEqual("let", statement.token_literal())
        self.assertEqual(ast.LetStatement, type(statement))
        self.assertEqual(name, statement.name.value)
        self.assertEqual(name, statement.name.token_literal())


if __name__ == '__main__':
    unittest.main()
