#Variable Partition Truth Assignment

import pycosat

def is_variable_partition_possible(formula, K):
    # Convert the formula to CNF format expected by pycosat
    cnf_formula = [list(clause) for clause in formula]

    # Duplicate the variables K times to create K disjoint sets
    cnf_formula_extended = []
    num_vars = max(abs(literal) for clause in cnf_formula for literal in clause)
    for i in range(K):
        offset = i * num_vars
        for clause in cnf_formula:
            cnf_formula_extended.append([literal + offset for literal in clause])

    # Solve the extended CNF formula using pycosat
    solution = pycosat.solve(cnf_formula_extended)

    # Check if the solution is satisfiable
    return solution != "UNSAT"

# Example usage
formula = [[1, -2, 3], [-1, 2, 3], [1, 2, -3]]  # CNF formula
K = 2  # Number of disjoint sets

is_possible = is_variable_partition_possible(formula, K)

if is_possible:
    print(f"It is possible to partition the variables of the formula into {K} disjoint sets.")
else:
    print(f"It is not possible to partition the variables of the formula into {K} disjoint sets.")
