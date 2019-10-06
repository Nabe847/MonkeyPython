from pmonkey.objects import Integer
import pmonkey.ast as ast

def eval(node):
    node_type = type(node)
    if node_type == ast.Program:
        return eval_statements(node.statements)
    elif node_type == ast.ExpressionStatement:
        return eval(node.expression)
    elif node_type == ast.IntegerLiteral:
        int_obj = Integer(node.value)
        return int_obj

def eval_statements(statements):
    for statement in statements:
        result = eval(statement)

    return result


