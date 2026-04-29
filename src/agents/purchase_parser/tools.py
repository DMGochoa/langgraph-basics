_ALLOWED = set("0123456789+-*/(). ")


def calculate_expression(expression: str) -> float:
    if not all(c in _ALLOWED for c in expression):
        raise ValueError(f"Invalid expression: {expression!r}")
    return float(eval(expression, {"__builtins__": {}}, {}))
