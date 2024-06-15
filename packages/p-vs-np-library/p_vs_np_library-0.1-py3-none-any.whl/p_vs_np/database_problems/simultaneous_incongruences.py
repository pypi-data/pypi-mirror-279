#Simultaneous Incongruences

from sympy import symbols, Eq, solve


def is_simultaneous_solution(equations):
    # Create symbols for unknown variables
    variables = symbols('x:%d' % len(equations))

    # Create a list of equations using the symbols
    eqs = [Eq(var, a, modulus=m) for var, a, m in equations]

    # Solve the simultaneous equations
    solution = solve(eqs, variables)

    # Check if a solution exists
    return bool(solution)


# Example usage
equations = [(symbols('x1'), 1, 3),
             (symbols('x2'), 2, 4),
             (symbols('x3'), 2, 5)]

has_solution = is_simultaneous_solution(equations)
print("A simultaneous solution exists:", has_solution)

