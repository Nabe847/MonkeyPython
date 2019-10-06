import unittest
from pmonkey.lexer import Lexer
from pmonkey.parser import Parser
from pmonkey import ast


# python -m unittest tests.test_ast
class TestParser(unittest.TestCase):
    def test_let_statements(self):
        tests = [
            {"input": "let x = 5;", "exp_identifier": "x", "exp_value": 5},
            {"input": "let y = true;", "exp_identifier": "y", "exp_value": True},
            {"input": "let foobar = y;", "exp_identifier": "foobar", "exp_value": "y"}
        ]

        for test in tests:
            l = Lexer(test["input"])
            parser = Parser(l)
            program = parser.parse_program()
            self.check_parser_errors(parser)

            self.assertEqual(1, len(program.statements))
            statement = program.statements[0]
            self.assert_let_statement(test["exp_identifier"], statement)
            self.assertEqual(test["exp_value"], statement.value.value)

    def test_return_statement(self):
        tests = [
            {"input": "return 5;",  "exp_value": 5},
            {"input": "return true;", "exp_value": True},
            {"input": "return y;", "exp_value": "y"},
        ]

        for test in tests:
            l = Lexer(test["input"])
            parser = Parser(l)
            program = parser.parse_program()
            self.check_parser_errors(parser)

            self.assertEqual(1, len(program.statements))
            statement = program.statements[0]
            self.assertEqual(ast.ReturnStatement, type(statement))
            self.assertEqual("return", statement.token_literal())
            self.assertEqual(test["exp_value"], statement.return_value.value)

    def test_identifier_expression(self):
        input = "foobar;"
        l = Lexer(input)
        parser = Parser(l)
        program = parser.parse_program()
        self.check_parser_errors(parser)

        self.assertEqual(1, len(program.statements))

        ident = program.statements[0].expression
        self.assert_expression(ast.Identifier, "foobar", "foobar", ident)

    def test_integer_literal_expression(self):
        input = "5;"
        l = Lexer(input)
        parser = Parser(l)
        program = parser.parse_program()
        self.check_parser_errors(parser)

        self.assertEqual(1, len(program.statements))

        literal = program.statements[0].expression
        self.assert_expression(ast.IntegerLiteral, 5, "5", literal)

    def test_boolean_literal_expression(self):
        tests = [
            ["true", "true"],
            ["false", "false"],
            ["3 > 5 == false", "((3>5)==false)"],
            ["3 < 5 == true", "((3<5)==true)"],
        ]

        for test in tests:
            l = Lexer(test[0])
            p = Parser(l)
            program = p.parse_program()

            self.assertEqual(1, len(program.statements))
            s = str(program)
            # print(s)
            self.assertEqual(test[1], s)

    def test_parsing_prefix_expressions(self):
        prefix_tests = [
            {"input": "!5;", "operator": "!",
                "value": 5, "type": ast.IntegerLiteral},
            {"input": "-15", "operator": "-",
                "value": 15, "type": ast.IntegerLiteral},
            {"input": "!true", "operator": "!",
                "value": True, "type": ast.BooleanLiteral},
            {"input": "!false", "operator": "!",
                "value": False, "type": ast.BooleanLiteral},
        ]

        # print()
        for test in prefix_tests:
            l = Lexer(test["input"])
            p = Parser(l)
            program = p.parse_program()
            self.check_parser_errors(p)

            self.assertEqual(1, len(program.statements))
            statement = program.statements[0]

            # print(str(program))

            self.assertEqual(ast.ExpressionStatement, type(statement))

            expression = statement.expression
            self.assertEqual(ast.PrefixExpression, type(expression))
            self.assertEqual(test["operator"], expression.operator)
            self.assert_literal(test["type"], test["value"], expression.right)

    def test_parsing_infix_expressions(self):
        integer = ast.IntegerLiteral
        bool = ast.BooleanLiteral
        infix_tests = [
            ["5+5;", 5, "+", 5, integer],
            ["5-5;", 5, "-", 5, integer],
            ["5*5;", 5, "*", 5, integer],
            ["5/5;", 5, "/", 5, integer],
            ["5>5;", 5, ">", 5, integer],
            ["5<5;", 5, "<", 5, integer],
            ["5==5;", 5, "==", 5, integer],
            ["5!=5;", 5, "!=", 5, integer],

            ["true == true", True, "==", True, bool],
            ["true != false", True, "!=", False, bool],
            ["false == false", False, "==", False, bool],
        ]

        # print()
        for test in infix_tests:
            l = Lexer(test[0])
            p = Parser(l)
            program = p.parse_program()
            self.check_parser_errors(p)

            self.assertEqual(1, len(program.statements))
            statement = program.statements[0]

            # print(str(program))

            self.assertEqual(ast.ExpressionStatement, type(statement))

            expression = statement.expression
            self.assertEqual(ast.InfixExpression, type(expression))
            self.assert_literal(test[4], test[1], expression.left)
            self.assertEqual(test[2], expression.operator)
            self.assert_literal(test[4], test[3], expression.right)

    def test_operator_precedence_parsing(self):
        tests = [
            [
                "-a * b",
                "((-a)*b)"
            ],
            [
                "!-a",
                "(!(-a))"
            ],
            [
                "a + b + c",
                "((a+b)+c)"
            ],
            [
                "a + b - c",
                "((a+b)-c)"
            ],
            [
                "a * b * c",
                "((a*b)*c)"
            ],
            [
                "a * b / c",
                "((a*b)/c)"
            ],
            [
                "a + b / c",
                "(a+(b/c))"
            ],
            [
                "a + b * c + d / e - f",
                "(((a+(b*c))+(d/e))-f)"
            ],
            [
                "3 + 4; -5 * 5",
                "(3+4)((-5)*5)"
            ],
            [
                "5 > 4 == 3 < 4",
                "((5>4)==(3<4))"
            ],
            [
                "5 < 4 != 3 > 4",
                "((5<4)!=(3>4))"
            ],
            [
                "3 + 4 * 5 == 3 * 1 + 4 * 5",
                "((3+(4*5))==((3*1)+(4*5)))"
            ],
            [
                "1 + (2 + 3) + 4",
                "((1+(2+3))+4)"
            ],
            [
                "(5 + 5) * 2",
                "((5+5)*2)"
            ],
            [
                "2 / (5 + 5)",
                "(2/(5+5))"
            ],
            [
                "-(5 + 5)",
                "(-(5+5))"
            ],
            [
                "!(true == false)",
                "(!(true==false))"
            ],
            [
                "a + add(b * c) + d",
                "((a+add((b*c)))+d)"
            ],
            [
                "add(a, b, 1, 2 * 3, 4 + 5, add(6, 7*8))",
                "add(a,b,1,(2*3),(4+5),add(6,(7*8)))"
            ],
            [
                "add(a+b+c*d/f+g)",
                "add((((a+b)+((c*d)/f))+g))"
            ],
        ]

        # print()
        for test in tests:
            l = Lexer(test[0])
            p = Parser(l)
            program = p.parse_program()
            self.check_parser_errors(p)

            s = str(program)
            # print(s)
            self.assertEqual(test[1], s)

    def test_if_expression(self):
        input = "if (x < y) { x }"
        l = Lexer(input)
        p = Parser(l)
        program = p.parse_program()
        self.check_parser_errors(p)

        self.assertEqual(1, len(program.statements))
        statement = program.statements[0]
        self.assertEqual(ast.ExpressionStatement, type(statement))

        expression = statement.expression
        self.assertEqual(ast.IfExpression, type(expression))

        condition = expression.condition
        self.assertEqual(ast.InfixExpression, type(condition))
        self.assert_literal(ast.Identifier, "x", condition.left)
        self.assertEqual("<", condition.operator)
        self.assert_literal(ast.Identifier, "y", condition.right)

        self.assertEqual(1, len(expression.consequence.statements))
        consequence = expression.consequence.statements[0]

        self.assertEqual(ast.ExpressionStatement, type(consequence))

        csq_exp = consequence.expression
        self.assertEqual(ast.Identifier, type(csq_exp))
        self.assertEqual("x", csq_exp.value)

    def test_if_else_expression(self):
        input = "if (x > y) { x } else { y }"
        l = Lexer(input)
        p = Parser(l)
        program = p.parse_program()
        self.check_parser_errors(p)

        self.assertEqual(1, len(program.statements))
        statement = program.statements[0]
        self.assertEqual(ast.ExpressionStatement, type(statement))

        if_exp = statement.expression
        self.assertEqual(ast.IfExpression, type(if_exp))

        alt_statement = if_exp.alternative
        self.assertEqual(ast.BlockStatement, type(alt_statement))
        self.assertEqual(1, len(alt_statement.statements))

        alt_exp = alt_statement.statements[0].expression
        self.assertEqual(ast.Identifier, type(alt_exp))
        self.assertEqual("y", alt_exp.value)

    def test_function_literal_parsing(self):
        input = "fn(x, y){ x + y }"
        l = Lexer(input)
        p = Parser(l)
        program = p.parse_program()
        self.check_parser_errors(p)

        self.assertEqual(1, len(program.statements))
        statement = program.statements[0]

        self.assertEqual(ast.ExpressionStatement, type(statement))
        function = statement.expression

        self.assertEqual(ast.FunctionLiteral, type(function))

        self.assertEqual(2, len(function.parameters))
        self.assert_literal(ast.Identifier, "x", function.parameters[0])
        self.assert_literal(ast.Identifier, "y", function.parameters[1])

        self.assertEqual(ast.BlockStatement, type(function.body))
        body = function.body
        self.assertEqual(1, len(body.statements))

        body_statement = body.statements[0]
        self.assertEqual(ast.ExpressionStatement, type(body_statement))
        infix = body_statement.expression
        self.assertEqual(ast.InfixExpression, type(infix))
        self.assert_literal(ast.Identifier, "x", infix.left)
        self.assertEqual("+", infix.operator)
        self.assert_literal(ast.Identifier, "y", infix.right)

    def test_function_parameter_parsing(self):
        tests = [
            {"input": "fn(){}", "expected_params": []},
            {"input": "fn(x){}", "expected_params": ["x"]},
            {"input": "fn(x,y,z){}", "expected_params": ["x", "y", "z"]},
        ]

        for test in tests:
            l = Lexer(test["input"])
            p = Parser(l)
            program = p.parse_program()
            self.check_parser_errors(p)

            statement = program.statements[0]
            function = statement.expression

            self.assertEqual(
                len(test["expected_params"]), len(function.parameters))

            for exp, act in zip(test["expected_params"], function.parameters):
                self.assertEqual(exp, act.value)

    def test_call_expression_parsing(self):
        input = "add(1, 2*3, 4+5)"

        l = Lexer(input)
        p = Parser(l)
        program = p.parse_program()
        self.check_parser_errors(p)

        self.assertEqual(1, len(program.statements))
        statement = program.statements[0]

        self.assertEqual(ast.ExpressionStatement, type(statement))
        self.assertEqual(ast.CallExpression, type(statement.expression))
        call_exp = statement.expression

        self.assertEqual(ast.Identifier, type(call_exp.function))
        self.assertEqual("add", call_exp.function.value)

        self.assertEqual(3, len(call_exp.arguments))

        self.assertEqual(ast.IntegerLiteral, type(call_exp.arguments[0]))
        self.assertEqual(1, call_exp.arguments[0].value)

        self.assertEqual(ast.InfixExpression, type(call_exp.arguments[1]))
        infix = call_exp.arguments[1]
        self.assertEqual(ast.IntegerLiteral, type(infix.left))
        self.assertEqual(2, infix.left.value)
        self.assertEqual("*", infix.operator)
        self.assertEqual(ast.IntegerLiteral, type(infix.right))
        self.assertEqual(3, infix.right.value)

        self.assertEqual(ast.InfixExpression, type(call_exp.arguments[2]))
        infix = call_exp.arguments[2]
        self.assertEqual(ast.IntegerLiteral, type(infix.left))
        self.assertEqual(4, infix.left.value)
        self.assertEqual("+", infix.operator)
        self.assertEqual(ast.IntegerLiteral, type(infix.right))
        self.assertEqual(5, infix.right.value)

    def assert_let_statement(self, name, statement):
        self.assertEqual("let", statement.token_literal())
        self.assertEqual(ast.LetStatement, type(statement))
        self.assertEqual(name, statement.name.value)
        self.assertEqual(name, statement.name.token_literal())

    def assert_literal(self, exp_type, exp_value, expression):
        self.assertEqual(exp_type, type(expression))
        self.assertEqual(exp_value, expression.value)

    def assert_expression(self, exp_type, exp_value, exp_literal, expression):
        self.assertEqual(exp_type, type(expression))
        self.assertEqual(exp_value, expression.value)
        self.assertEqual(exp_literal, expression.token_literal())

    def check_parser_errors(self, parser):
        if len(parser.errors) == 0:
            return

        print()
        for msg in parser.errors:
            print(f"parser error: {msg}")

        self.fail()
