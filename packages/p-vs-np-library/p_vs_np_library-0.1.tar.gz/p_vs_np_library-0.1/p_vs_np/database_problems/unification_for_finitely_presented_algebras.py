#Unification for finitely presented algebras


def unify_equations(equations):
    equations = list(equations)  # Convert equations to a list

    # Check if the equations list is empty
    if len(equations) == 0:
        return True

    # Choose the first equation from the list
    equation = equations[0]

    # Check if the equation is of the form "t = t"
    if equation[0] == equation[1]:
        return unify_equations(equations[1:])

    # Check if the equation is of the form "v = t"
    if isinstance(equation[0], str):
        var = equation[0]
        term = equation[1]
        if var in term:
            return False
        new_equations = [(substitute(var, term, eq[0]), substitute(var, term, eq[1])) for eq in equations[1:]]
        return unify_equations(new_equations)

    # Check if the equation is of the form "t = v"
    if isinstance(equation[1], str):
        var = equation[1]
        term = equation[0]
        if var in term:
            return False
        new_equations = [(substitute(var, term, eq[0]), substitute(var, term, eq[1])) for eq in equations[1:]]
        return unify_equations(new_equations)

    # Check if the equation is of the form "f(t1, t2, ..., tn) = f(u1, u2, ..., um)"
    if equation[0][0] == equation[1][0]:
        args1 = equation[0][1:]
        args2 = equation[1][1:]
        if len(args1) != len(args2):
            return False
        new_equations = [(args1[i], args2[i]) for i in range(len(args1))]
        return unify_equations(new_equations + equations[1:])

    # No unification is possible
    return False

def substitute(var, term, expression):
    if expression == var:
        return term
    elif isinstance(expression, list):
        return [substitute(var, term, sub_expr) for sub_expr in expression]
    else:
        return expression

# Example usage
equations = [(['f', 'x'], 'y'), (['f', 'y'], 'x')]
result = unify_equations(equations)

if result:
    print("Equations have a common solution.")
else:
    print("Equations do not have a common solution.")

