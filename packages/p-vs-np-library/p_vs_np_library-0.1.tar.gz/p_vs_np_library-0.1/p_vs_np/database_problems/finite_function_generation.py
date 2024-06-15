#Finite Function Generation

from itertools import product

def compose_functions(f, g):
    return lambda x: f(g(x))

def can_generate_function(F, h):
    n = len(F)
    for composition_length in range(1, n + 1):
        for composition in product(F, repeat=composition_length):
            composed_function = composition[0]
            for i in range(1, composition_length):
                composed_function = compose_functions(composed_function, composition[i])
            if composed_function == h:
                return True
    return False

# Example usage
def f1(x):
    return x + 1

def f2(x):
    return x * 2

def f3(x):
    return x - 1

F = [f1, f2, f3]
h = lambda x: x * 3 - 1

if can_generate_function(F, h):
    print("Function h can be generated from the functions in F.")
else:
    print("Function h cannot be generated from the functions in F.")

