#Comparative Divisibility

from sympy import symbols, Poly, congruence, Eq, solve


def is_comparative_divisible(equations, comparative_relations):
    # Create symbols for unknown variables
    variables = symbols('x:%d' % len(equations))

    # Create a list of congruence equations
    congruences = []
    for equation in equations:
        f_x, g_x, m = equation
        f_polynomial = Poly(f_x)
        g_polynomial = Poly(g_x)
        congruences.append(Eq(f_polynomial, g_polynomial) % m)

    # Solve the system of equations
    solution = solve(congruences, variables)

    # Check comparative relations
    for relation in comparative_relations:
        x_i, x_j = relation
        if solution[x_i] >= solution[x_j]:
            return False

    return True


# Example usage
equations = [('2*x + 1', 'x', 3),
             ('3*x - 1', '2*x', 4)]
comparative_relations = [(0, 1)]

is_divisible = is_comparative_divisible(equations, comparative_relations)
print("A solution satisfying comparative divisibility exists:", is_divisible)

