import ast
import operator


ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def evaluate_expression(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numbers are allowed.")

    if isinstance(node, ast.BinOp):
        left = evaluate_expression(node.left)
        right = evaluate_expression(node.right)
        operator_type = type(node.op)

        if operator_type not in ALLOWED_OPERATORS:
            raise ValueError("Operator not allowed.")

        return ALLOWED_OPERATORS[operator_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = evaluate_expression(node.operand)
        operator_type = type(node.op)

        if operator_type not in ALLOWED_OPERATORS:
            raise ValueError("Operator not allowed.")

        return ALLOWED_OPERATORS[operator_type](operand)

    raise ValueError("Invalid expression.")


def calculator_tool(expression: str) -> dict:
    try:
        tree = ast.parse(expression, mode="eval")
        result = evaluate_expression(tree.body)

        return {
            "tool_name": "calculator",
            "result": str(result)
        }

    except Exception as e:
        return {
            "tool_name": "calculator",
            "result": f"Calculation error: {e}"
        }