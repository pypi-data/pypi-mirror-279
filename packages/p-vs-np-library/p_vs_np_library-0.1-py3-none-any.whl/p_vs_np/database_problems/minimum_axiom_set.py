#Minimum Axiom Set

import itertools


class Axiom:
    def __init__(self, statement):
        self.statement = statement

    def __repr__(self):
        return self.statement


class Theorem:
    def __init__(self, statement):
        self.statement = statement

    def __repr__(self):
        return self.statement


def is_provable(theorems, axiom_set):
    for theorem in theorems:
        if not prove_theorem(theorem, axiom_set):
            return False
    return True


def prove_theorem(theorem, axiom_set):
    if theorem in axiom_set:
        return True

    for axiom in axiom_set:
        if is_theorem_from_axiom(theorem, axiom_set, axiom):
            return True

    return False


def is_theorem_from_axiom(theorem, axiom_set, axiom):
    # Assume the theorem is a string representation of a propositional logic formula
    # and axiom_set is a list of Axiom objects.
    # Here, we are using a simple evaluation method to determine if the theorem can be derived from the axiom.

    variables = set(theorem)
    variable_assignments = list(itertools.product([True, False], repeat=len(variables)))

    for assignment in variable_assignments:
        assignment_dict = {variable: value for variable, value in zip(variables, assignment)}

        if evaluate_formula(theorem, axiom_set, assignment_dict):
            return True

    return False


def evaluate_formula(formula, axiom_set, assignment):
    # Evaluate the formula based on the axiom_set and the variable assignment.
    # This implementation assumes the formula is in propositional logic with basic logical operators.

    stack = []
    for symbol in formula:
        if symbol.isalpha():
            stack.append(assignment[symbol])
        elif symbol == '~':
            stack.append(not stack.pop())
        elif symbol == '→':
            rhs = stack.pop()
            lhs = stack.pop()
            stack.append(not lhs or rhs)
        elif symbol == '↔':
            rhs = stack.pop()
            lhs = stack.pop()
            stack.append(lhs == rhs)

    return stack[0]


# Example usage
axioms = [
    Axiom("p → (q → p)"),
    Axiom("(p → (q → r)) → ((p → q) → (p → r))"),
    Axiom("(~q → ~p) → (p → q)"),
    Axiom("(p → q) ∨ (q → p)")
]

theorems = [
    Theorem("p → p"),
    Theorem("(p → q) → ((q → r) → (p → r))"),
    Theorem("(p → q) ∨ (q → p)"),
    Theorem("p → (q → p)")
]

# Generate all possible axiom sets
axiom_sets = []
for r in range(len(axioms) + 1):
    for combination in itertools.combinations(axioms, r):
        axiom_sets.append(list(combination))

# Find the minimum axiom set that proves all the theorems
minimum_axiom_set = None
for axiom_set in axiom_sets:
    if is_provable(theorems, axiom_set):
        minimum_axiom_set = axiom_set
        break

if minimum_axiom_set:
    print("Minimum Axiom Set:")
    for axiom in minimum_axiom_set:
        print(axiom)
else:
    print("No axiom set found to prove all the theorems.")

