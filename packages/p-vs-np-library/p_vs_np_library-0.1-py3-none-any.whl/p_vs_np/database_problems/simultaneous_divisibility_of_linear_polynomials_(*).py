#Simultaneous Divisibility of Linear Polynomials(*)

from sympy import symbols, Poly, congruence


def is_simultaneous_solution(equations):
    # Create symbols for unknown variables
    variables = symbols('x:%d' % len(equations))

    # Create a list of congruence equations
    congruences = []
    for equation in equations:
        f_x, m = equation
        polynomial = Poly(f_x)
        congruences.append(congruence(polynomial, 0, modulus=m))

    # Check if a simultaneous solution exists
    solution = congruences[0].solve(variables, modulus=None)
    for congruence in congruences[1:]:
        if not congruence.contains(solution):
            return False

    return True


# Example usage
equations = [('2*x + 1', 3),
             ('3*x - 1', 4),
             ('x + 2', 5)]

has_solution = is_simultaneous_solution(equations)
print("A simultaneous solution exists:", has_solution)

