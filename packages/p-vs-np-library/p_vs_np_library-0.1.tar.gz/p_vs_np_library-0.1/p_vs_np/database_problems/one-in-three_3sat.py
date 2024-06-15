#One-In-Three 3SAT

def is_satisfiable(clauses, assignment):
    # Base case: all clauses are satisfied
    if all(evaluate_clause(clause, assignment) for clause in clauses):
        return True

    # Base case: conflicting assignment
    if any(evaluate_clause(clause, assignment) == False for clause in clauses):
        return False

    # Choose a variable to assign
    var = choose_variable(assignment)

    # Try assigning True to the variable
    assignment[var] = True
    if is_satisfiable(clauses, assignment):
        return True

    # Try assigning False to the variable
    assignment[var] = False
    if is_satisfiable(clauses, assignment):
        return True

    # Backtrack
    assignment[var] = None

    return False


def evaluate_clause(clause, assignment):
    # Evaluate a single clause based on the given assignment

    true_literals = 0

    for literal in clause:
        var, negated = abs(literal), literal < 0
        if assignment[var] == (not negated):
            true_literals += 1

    return true_literals == 1


def choose_variable(assignment):
    # Choose an unassigned variable to assign

    for var, value in assignment.items():
        if value is None:
            return var

    return None


# Example usage
clauses = [
    [1, 2, 3],
    [-1, -2, 4],
    [3, -4, -5],
    [-3, 5, 6]
]

# Initialize the assignment dictionary
assignment = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None}

if is_satisfiable(clauses, assignment):
    print("Satisfiable: Yes")
    satisfying_assignment = {var: value for var, value in assignment.items() if value is not None}
    print("Satisfying assignment:", satisfying_assignment)
else:
    print("Satisfiable: No")
