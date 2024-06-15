#Tableau Equivalence

import itertools

def is_tableau_equivalent(formula1, formula2):
    variables = get_variables(formula1, formula2)
    truth_table1 = generate_truth_table(formula1, variables)
    truth_table2 = generate_truth_table(formula2, variables)

    return all(truth_table1[var] == truth_table2[var] for var in variables)

def get_variables(formula1, formula2):
    variables1 = set(get_formula_variables(formula1))
    variables2 = set(get_formula_variables(formula2))
    return variables1.union(variables2)

def get_formula_variables(formula):
    variables = []
    for token in formula:
        if token.isalpha() and token.islower():
            variables.append(token)
    return variables

def generate_truth_table(formula, variables):
    truth_table = {}

    for assignment in itertools.product([False, True], repeat=len(variables)):
        assignment_dict = dict(zip(variables, assignment))
        truth_table_key = ''.join(str(int(assignment_dict[var])) for var in variables)
        truth_table[truth_table_key] = evaluate_formula(formula, assignment_dict)

    return truth_table

def evaluate_formula(formula, assignment):
    stack = []
    for token in formula:
        if token.isalpha() and token.islower():
            stack.append(assignment[token])
        elif token == '~':
            value = stack.pop()
            stack.append(not value)
        elif token in ['&', '|', '^']:
            value2 = stack.pop()
            value1 = stack.pop()
            stack.append(evaluate_operator(token, value1, value2))

    return stack.pop()

def evaluate_operator(operator, value1, value2):
    if operator == '&':
        return value1 and value2
    elif operator == '|':
        return value1 or value2
    elif operator == '^':
        return value1 != value2

# Example usage
formula1 = ['p', '&', 'q']
formula2 = ['q', '&', 'p']

result = is_tableau_equivalent(formula1, formula2)
if result:
    print("Formulas are equivalent.")
else:
    print("Formulas are not equivalent.")
