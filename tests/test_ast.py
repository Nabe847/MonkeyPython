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
        parser = Parser(l)
        program = parser.parse_program()
        self.check_parser_errors(parser)

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

    def test_return_statement(self):
        input = """
        return 5;
        return 10;
        return 9993332;
        """

        l = Lexer(input)
        parser = Parser(l)
        program = parser.parse_program()
        self.check_parser_errors(parser)

        self.assertEqual(3, len(program.statements))

        for statement in program.statements:
            self.assertEqual("return", statement.token_literal())
            self.assertEqual(ast.ReturnStatement, type(statement))

    def test_identifier_expression(self):
        input = "foobar;"
        l = Lexer(input)
        parser = Parser(l)
        program = parser.parse_program()
        self.check_parser_errors(parser)
        self.assertEqual(1, len(program.statements))
        ident = program.statements[0].expression
        self.assertEqual(ast.Identifier, type(ident))
        self.assertEqual("foobar", ident.value)
        self.assertEqual("foobar", ident.token_literal())

    def test_integer_literal_expression(self):
        input = "5;"
        l = Lexer(input)
        parser = Parser(l)
        program = parser.parse_program()
        self.check_parser_errors(parser)
        self.assertEqual(1, len(program.statements))
        literal = program.statements[0].expression
        self.assertEqual(ast.IntegerLiteral, type(literal))
        self.assertEqual(5, literal.value)
        self.assertEqual("5", literal.token_literal())

    def test_parsing_prefix_expressions(self):
        prefix_tests = [
            {"input":"!5;", "operator":"!", "integer_value":5},
            {"input":"-15", "operator":"-", "integer_value":15},
        ]

        for test in prefix_tests:
            l = Lexer(test["input"])
            p = Parser(l)
            program = p.parse_program()
            self.check_parser_errors(p)

            self.assertEqual(1, len(program.statements))
            statement = program.statements[0]
            self.assertEqual(ast.ExpressionStatement, type(statement))

            expression = statement.expression
            self.assertEqual(ast.PrefixExpression, type(expression))
            self.assertEqual(test["operator"], expression.operator)
            self.assert_integer_literal(
                test["integer_value"], expression.right)
        
    def assert_integer_literal(self, expected, expression):
        self.assertEqual(ast.IntegerLiteral, type(expression))
        self.assertEqual(expected, expression.value)
        self.assertEqual(str(expected), expression.token_literal())

    def check_parser_errors(self, parser):
        if len(parser.errors) == 0:
            return

        for msg in parser.errors:
            print(f"parser error: {msg}")

        self.fail()


if __name__ == '__main__':
    unittest.main()
