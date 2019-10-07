import unittest
from pmonkey.lexer import Lexer
from pmonkey.parser import Parser
from pmonkey.objects import Integer
from pmonkey.objects import Boolean
from pmonkey.objects import Null
from pmonkey.objects import Error
import pmonkey.evaluator as evaluator


# python -m unittest tests.test_evaluator
class TestEvaluator(unittest.TestCase):
    def test_eval_integer_expression(self):
        tests = [
            ["5", 5],
            ["10", 10],
            ["-5", -5],
            ["-10", -10],
            ["5 + 5 + 5 + 5 - 10", 10],
            ["2 * 2 * 2 * 2 * 2", 32],
            ["-50 + 100 - 50", 0],
            ["5 * 2 + 10", 20],
            ["5 + 2 * 10", 25],
            ["20 + 2 * -10", 0],
            ["50 / 2 * 2 + 10", 60],
            ["2 * (5 + 10)", 30],
            ["3 * 3 * 3 + 10", 37],
            ["3 * (3 * 3) + 10", 37],
            ["(5 + 10 * 2 + 15 / 3) * 2 + -10", 50],
        ]

        for s, exp_value in tests:
            obj = self.eval(s)
            self.assert_integer_object(exp_value, obj)

    def test_eval_boolean_expression(self):
        tests = [
            ["true", True],
            ["false", False],
        ]

        for s, exp_value in tests:
            obj = self.eval(s)
            self.assert_boolean_object(exp_value, obj)

    def test_bang_operator(self):
        tests = [
            ["!true", False],
            ["!false", True],
            ["!5", False],
            ["!!true", True],
            ["!!false", False],
            ["!!5", True],
            ["1 < 2", True],
            ["1 > 2", False],
            ["1 < 1", False],
            ["1 == 1", True],
            ["1 != 1", False],
            ["1 == 2", False],
            ["1 != 2", True],
            ["true == true", True],
            ["false == false", True],
            ["true == false", False],
            ["true != false", True],
            ["(1 < 2) == true", True],
            ["(1 < 2) == false", False],
            ["(1 > 2) == true", False],
            ["(1 > 2) == false", True],
        ]

        for s, exp_value in tests:
            obj = self.eval(s)
            self.assert_boolean_object(exp_value, obj)

    def test_if_else_expressions(self):
        tests = [
            ["if(true){ 10 }", 10],
            ["if(false){ 10 }", None],
            ["if(1){ 10 }", 10],
            ["if(1 < 2){ 10 }", 10],
            ["if(1 > 2){ 10 }", None],
            ["if(1 > 2){ 10 } else { 20 }", 20],
            ["if(1 < 2){ 10 } else { 20 }", 10],
        ]

        for s, exp_value in tests:
            evaluated = self.eval(s)
            if exp_value:
                self.assert_integer_object(exp_value, evaluated)
            else:
                self.assertEqual(Null, type(evaluated))

    def test_return_statements(self):
        tests = [
            ["return 10;", 10],
            ["return 10; 9;", 10],
            ["return 2 * 5; 9;", 10],
            ["9; return 2 * 5; 9;", 10],
            [
                """
                if(10 > 1){
                    if(10 > 1){
                        return 10;
                    }
                    return 1
                }
                """,
                10
            ],
        ]

        for s, exp_value in tests:
            evaluated = self.eval(s)
            self.assert_integer_object(exp_value, evaluated)

    def test_error_handling(self):
        tests = [
            ["5 + true", "type mismatch: INTEGER + BOOLEAN"],
            ["5 + true; 5", "type mismatch: INTEGER + BOOLEAN"],
            ["-true", "unknown operator: -BOOLEAN"],
            ["true + false", "unknown operator: BOOLEAN + BOOLEAN"],
            ["5; true + false; 5", "unknown operator: BOOLEAN + BOOLEAN"],
            ["if (10 > 1) { true + false; }",
             "unknown operator: BOOLEAN + BOOLEAN"],
            [
                """
                if(10 > 1){
                    if(10 > 1){
                        return true + false;
                    }
                    return 1;
                }
                """,
                "unknown operator: BOOLEAN + BOOLEAN"
            ],
        ]

        for test, exp_value in tests:
            evaluated = self.eval(test)
            self.assertEqual(Error, type(evaluated))
            self.assertEqual(exp_value, evaluated.message)

    def eval(self, input_str):
        l = Lexer(input_str)
        p = Parser(l)
        prg = p.parse_program()
        obj = evaluator.eval(prg)
        return obj

    def assert_boolean_object(self, exp_value, obj):
        self.assertEqual(Boolean, type(obj))
        self.assertEqual(exp_value, obj.value)

    def assert_integer_object(self, exp_value, obj):
        self.assertEqual(Integer, type(obj))
        self.assertEqual(exp_value, obj.value)
