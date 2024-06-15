#Modal Logic Provability

import itertools


class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class BoxOperator:
    def __init__(self, formula):
        self.formula = formula

    def __repr__(self):
        return f"□({self.formula})"


class DiamondOperator:
    def __init__(self, formula):
        self.formula = formula

    def __repr__(self):
        return f"◇({self.formula})"


def is_formula_provable(formula, worlds, relations):
    for assignment in itertools.product([False, True], repeat=len(worlds)):
        assignment_dict = dict(zip(worlds, assignment))
        if not evaluate_formula(formula, assignment_dict, relations):
            return False

    return True


def evaluate_formula(formula, assignment, relations):
    if isinstance(formula, Variable):
        return assignment[formula]

    if isinstance(formula, BoxOperator):
        subformula = formula.formula
        return all(evaluate_formula(subformula, assignment, relations[world])
                   for world in relations.keys())

    if isinstance(formula, DiamondOperator):
        subformula = formula.formula
        return any(evaluate_formula(subformula, assignment, relations[world])
                   for world in relations.keys())


# Example usage
worlds = ["w1", "w2"]
relations = {
    "w1": ["w1", "w2"],
    "w2": ["w1", "w2"]
}

formula = BoxOperator(
    DiamondOperator(
        Variable("w1")
    )
)

is_provable = is_formula_provable(formula, worlds, relations)
print("Is formula provable:", is_provable)
