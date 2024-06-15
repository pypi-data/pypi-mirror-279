#Sequential Truth Assignment

import pycosat

def is_satisfiable(formula):
    # Convert the formula to CNF format expected by pycosat
    cnf_formula = [list(clause) for clause in formula]

    # Solve the CNF formula using pycosat
    solution = pycosat.solve(cnf_formula)

    # Check if the solution is satisfiable
    return solution != "UNSAT"

# Example usage
formula = [[1, -2, 3], [-1, 2, 3], [1, 2, -3]]  # CNF formula

is_satisfiable = is_satisfiable(formula)

if is_satisfiable:
    print("The formula has a satisfying sequential truth assignment.")
else:
    print("The formula does not have a satisfying sequential truth assignment.")

