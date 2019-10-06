import unittest
from pmonkey.lexer import Lexer
from pmonkey.parser import Parser
from pmonkey.objects import Integer
from pmonkey.objects import Boolean
import pmonkey.evaluator as evaluator


# python -m unittest tests.test_evaluator
class TestEvaluator(unittest.TestCase):
    def test_eval_integer_expression(self):
        tests = [
            ["5", 5],
            ["10", 10],
            ["-5", -5],
            ["-10", -10],
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
        ]

        for s, exp_value in tests:
            obj = self.eval(s)
            self.assert_boolean_object(exp_value, obj)

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
