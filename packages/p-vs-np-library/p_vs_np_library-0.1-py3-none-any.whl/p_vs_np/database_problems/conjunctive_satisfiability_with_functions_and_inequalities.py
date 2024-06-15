#Conjunctive Satisfiability with Functions and Inequalities

import itertools


class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Function:
    def __init__(self, name, arity):
        self.name = name
        self.arity = arity

    def __repr__(self):
        return self.name


class Literal:
    def __init__(self, variable, negated=False):
        self.variable = variable
        self.negated = negated

    def __repr__(self):
        return f"{'~' if self.negated else ''}{self.variable}"


class Atom:
    def __init__(self, function, arguments, inequality=False):
        self.function = function
        self.arguments = arguments
        self.inequality = inequality

    def __repr__(self):
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f"{self.function}({args_str})" + (">" if self.inequality else "")


def is_formula_satisfiable(formula):
    variables = set()
    functions = set()
    literals = []

    for clause in formula:
        literals.extend(clause)

        for literal in clause:
            if isinstance(literal, Literal):
                variables.add(literal.variable)
            elif isinstance(literal, Atom):
                functions.add(literal.function)
                variables.update(literal.arguments)

    domain = [True, False]
    variable_assignments = list(itertools.product(domain, repeat=len(variables)))

    for assignment in variable_assignments:
        assignment_dict = {variable: value for variable, value in zip(variables, assignment)}

        if evaluate_formula(formula, assignment_dict):
            return True

    return False


def evaluate_formula(formula, assignment):
    for clause in formula:
        clause_result = any(evaluate_literal(literal, assignment) for literal in clause)
        if not clause_result:
            return False

    return True


def evaluate_literal(literal, assignment):
    if isinstance(literal, Literal):
        value = assignment[literal.variable]
        return value if not literal.negated else not value

    if isinstance(literal, Atom):
        args = [assignment[arg] for arg in literal.arguments]

        if literal.inequality:
            return args[0] > args[1]
        else:
            return args[0] == args[1]

    return False


# Example usage
variable_x = Variable("x")
variable_y = Variable("y")
function_f = Function("f", 1)
function_g = Function("g", 2)

# Example formula: (x ∨ ~y) ∧ (f(x) > g(y, x))
formula = [
    [Literal(variable_x), Literal(variable_y, negated=True)],
    [Atom(function_f, [variable_x]), Atom(function_g, [variable_y, variable_x], inequality=True)]
]

is_satisfiable = is_formula_satisfiable(formula)
print("Is formula satisfiable:", is_satisfiable)

