#Integer expression membership

def evaluate_expression(expression, value):
    if isinstance(expression, int):
        return expression == value
    elif isinstance(expression, str):
        return False  # Variables are not allowed in this problem
    else:
        operator = expression[0]
        operands = expression[1:]

        if operator == '+':
            return any(evaluate_expression(operand, value) for operand in operands)
        elif operator == '*':
            return all(evaluate_expression(operand, value) for operand in operands)
        elif operator == '-':
            return evaluate_expression(operands[0], value) and not evaluate_expression(operands[1], value)
        elif operator == '/':
            return evaluate_expression(operands[0], value) and evaluate_expression(operands[1], value)

    return False

# Example usage
expression = ['+', ['-', 10, 5], ['*', 3, 2]]
value = 9

if evaluate_expression(expression, value):
    print(f"The value {value} is a member of the set defined by the expression.")
else:
    print(f"The value {value} is not a member of the set defined by the expression.")

