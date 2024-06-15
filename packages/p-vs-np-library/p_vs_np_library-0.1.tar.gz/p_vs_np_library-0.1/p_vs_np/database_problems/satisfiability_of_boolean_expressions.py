#Satisfiability of boolean expressions

def evaluate_expression(expression, assignment):
    stack = []

    for token in expression:
        if token in ['AND', 'OR']:
            operand2 = stack.pop()
            operand1 = stack.pop()

            if token == 'AND':
                result = operand1 and operand2
            else:
                result = operand1 or operand2

            stack.append(result)
        else:
            variable = token[1:]

            if token[0] == '-':
                value = not assignment[variable]
            else:
                value = assignment[variable]

            stack.append(value)

    return stack.pop()


def solve_boolexp(expression, variables):
    assignment = {}
    return backtrack(expression, variables, assignment, 0)


def backtrack(expression, variables, assignment, index):
    if index == len(variables):
        return evaluate_expression(expression, assignment)

    variable = variables[index]

    assignment[variable] = True
    if backtrack(expression, variables, assignment, index + 1):
        return True

    assignment[variable] = False
    if backtrack(expression, variables, assignment, index + 1):
        return True

    del assignment[variable]
    return False


# Example usage
expression = ['AND', ['OR', 'x1', '-x2'], ['-x1', 'x2']]
variables = ['x1', 'x2']

result = solve_boolexp(expression, variables)

if result:
    print("Satisfying assignment exists")
else:
    print("No satisfying assignment exists")

