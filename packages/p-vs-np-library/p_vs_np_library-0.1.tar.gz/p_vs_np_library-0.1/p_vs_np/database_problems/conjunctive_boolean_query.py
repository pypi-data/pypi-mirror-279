#Conjunctive Boolean Query

def is_conjunctive_query_satisfiable(variables, formula):
    assignment = {}
    return is_formula_satisfiable(variables, formula, assignment)

def is_formula_satisfiable(variables, formula, assignment):
    if len(formula) == 0:
        return True

    clause = formula[0]
    remaining_formula = formula[1:]

    for literal in clause:
        var = literal[1:]  # Remove the negation symbol if present
        if literal.startswith('~'):
            assignment[var] = False
        else:
            assignment[var] = True

        if is_clause_satisfiable(variables, formula, assignment):
            return True

        assignment.pop(var)

    return False

def is_clause_satisfiable(variables, formula, assignment):
    for clause in formula:
        clause_satisfiable = False

        for literal in clause:
            var = literal[1:]  # Remove the negation symbol if present
            if literal.startswith('~'):
                if var in assignment and not assignment[var]:
                    clause_satisfiable = True
                    break
            else:
                if var in assignment and assignment[var]:
                    clause_satisfiable = True
                    break

        if not clause_satisfiable:
            return False

    return True

# Example usage
variables = ['A', 'B', 'C']
formula = [[~A, B], [~B, C], [C]]

result = is_conjunctive_query_satisfiable(variables, formula)
if result:
    print("Conjunctive boolean query is satisfiable.")
else:
    print("Conjunctive boolean query is not satisfiable.")

