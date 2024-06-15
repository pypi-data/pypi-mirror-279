#Inequivalence of simple functions

def are_functions_inequivalent(f, g, domain):
    for x in domain:
        if f(x) != g(x):
            return True

    return False

# Example usage
def square(x):
    return x ** 2

def double(x):
    return 2 * x

domain = range(10)

if are_functions_inequivalent(square, double, domain):
    print("Functions are inequivalent")
else:
    print("Functions are equivalent")

