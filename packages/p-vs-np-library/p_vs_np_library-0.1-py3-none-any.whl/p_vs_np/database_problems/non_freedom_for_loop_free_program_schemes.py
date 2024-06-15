#Non Freedom For Loop Free Program Schemes

import itertools

def generate_program_schemes(variables, size):
    schemes = []
    for scheme_size in range(1, size + 1):
        for scheme in itertools.product(variables, repeat=scheme_size):
            schemes.append(scheme)
    return schemes

def contains_for_loop(scheme):
    for statement in scheme:
        if statement.startswith('for'):
            return True
    return False

def solve_non_freedom_program_schemes(variables, size):
    schemes = generate_program_schemes(variables, size)
    for scheme in schemes:
        if not contains_for_loop(scheme):
            return scheme
    return None

# Example usage
variables = ['x', 'y', 'z']
size = 3

solution = solve_non_freedom_program_schemes(variables, size)
if solution is not None:
    print("Solution found:")
    print(solution)
else:
    print("No solution found.")
