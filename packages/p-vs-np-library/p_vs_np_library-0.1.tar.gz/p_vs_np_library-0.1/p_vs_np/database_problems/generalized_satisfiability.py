#Generalized Satisfiability

def solve_gensat(clauses, n_variables):
    assignment = [None] * n_variables
    return backtrack(clauses, assignment, 0)


def backtrack(clauses, assignment, index):
    if index == len(assignment):
        return True

    for value in [True, False]:
        assignment[index] = value

        if is_consistent(clauses, assignment):
            if backtrack(clauses, assignment, index + 1):
                return True

    assignment[index] = None
    return False


def is_consistent(clauses, assignment):
    for clause in clauses:
        clause_satisfied = False

        for literal in clause:
            var = abs(literal)
            value = literal > 0

            if assignment[var - 1] == value:
                clause_satisfied = True
                break

        if not clause_satisfied:
            return False

    return True


# Example usage
clauses = [
    [1, 2, -3],
    [1, -2, 3],
    [-1, 2, 3],
    [-1, -2, -3]
]
n_variables = 3

result = solve_gensat(clauses, n_variables)

if result:
    print("Satisfying assignment exists")
else:
    print("No satisfying assignment exists")
