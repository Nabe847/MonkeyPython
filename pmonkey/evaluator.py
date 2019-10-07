import pmonkey.objects as obj
from pmonkey.objects import Integer
from pmonkey.objects import Boolean
from pmonkey.objects import Null
from pmonkey.objects import ReturnValue
from pmonkey.objects import Error
import pmonkey.ast as ast

TRUE = Boolean(True)
FALSE = Boolean(False)
NULL = Null()


def eval(node):
    node_type = type(node)
    if node_type == ast.Program:
        return eval_program(node.statements)
    elif node_type == ast.ExpressionStatement:
        return eval(node.expression)
    elif node_type == ast.IntegerLiteral:
        int_obj = Integer(node.value)
        return int_obj
    elif node_type == ast.BooleanLiteral:
        bool_obj = native_boolean_to_boolean_object(node.value)
        return bool_obj
    elif node_type == ast.PrefixExpression:
        right = eval(node.right)
        if is_error(right):
            return right
        return eval_prefix_expression(node.operator, right)
    elif node_type == ast.InfixExpression:
        left = eval(node.left)
        if is_error(left):
            return left

        right = eval(node.right)
        if is_error(right):
            return right

        return eval_infix_expression(node.operator, left, right)
    elif node_type == ast.BlockStatement:
        return eval_block_statement(node.statements)
    elif node_type == ast.IfExpression:
        return eval_if_expression(node)
    elif node_type == ast.ReturnStatement:
        val = eval(node.return_value)
        if is_error(val):
            return val
        return ReturnValue(val)
    else:
        return NULL


def eval_program(statements):
    for statement in statements:
        result = eval(statement)
        if result.type() == obj.RETURN_VALUE_OBJ:
            return result.value
        elif result.type() == obj.ERROR_OBJ:
            return result

    return result


def eval_block_statement(statements):
    for statement in statements:
        result = eval(statement)

        if result.type() == obj.RETURN_VALUE_OBJ or result.type() == obj.ERROR_OBJ:
            return result

    return result


def eval_prefix_expression(op, right):
    if op == "!":
        return eval_bang_operator_expression(right)
    elif op == "-":
        return eval_minus_prefix_operator_expression(right)
    else:
        return Error(f"unknown operator: {op}{right.type()}")


def eval_infix_expression(op, left, right):
    if type(left) == Integer and type(right) == Integer:
        return eval_integer_infix_expression(op, left, right)
    elif op == "==":
        return native_boolean_to_boolean_object(left == right)
    elif op == "!=":
        return native_boolean_to_boolean_object(left != right)
    elif left.type() != right.type():
        return Error(f"type mismatch: {left.type()} {op} {right.type()}")
    else:
        return Error(f"unknown operator: {left.type()} {op} {right.type()}")


def eval_bang_operator_expression(right):
    if right == TRUE:
        return FALSE
    elif right == FALSE:
        return TRUE
    elif right == NULL:
        return TRUE
    else:
        return FALSE


def eval_minus_prefix_operator_expression(right):
    if type(right) != Integer:
        return Error(f"unknown operator: -{right.type()}")

    value = right.value
    return Integer(-value)


def eval_integer_infix_expression(op, left, right):
    if op == "+":
        return Integer(left.value + right.value)
    elif op == "-":
        return Integer(left.value - right.value)
    elif op == "*":
        return Integer(left.value * right.value)
    elif op == "/":
        return Integer(left.value / right.value)
    elif op == "<":
        return native_boolean_to_boolean_object(left.value < right.value)
    elif op == ">":
        return native_boolean_to_boolean_object(left.value > right.value)
    elif op == "==":
        return native_boolean_to_boolean_object(left.value == right.value)
    elif op == "!=":
        return native_boolean_to_boolean_object(left.value != right.value)
    else:
        return Error(f"unknown operator: {left.type()} {op} {right.type()}")


def eval_if_expression(node):
    condition = eval(node.condition)
    if is_error(condition):
        return condition
        
    if is_truthy(condition):
        return eval(node.consequence)
    elif node.alternative:
        return eval(node.alternative)
    else:
        return NULL


def is_truthy(value):
    if value == NULL:
        return False
    elif value == TRUE:
        return True
    elif value == FALSE:
        return False
    else:
        return True


def native_boolean_to_boolean_object(boolean_value):
    return TRUE if boolean_value else FALSE


def is_error(node):
    return node.type() == obj.ERROR_OBJ
