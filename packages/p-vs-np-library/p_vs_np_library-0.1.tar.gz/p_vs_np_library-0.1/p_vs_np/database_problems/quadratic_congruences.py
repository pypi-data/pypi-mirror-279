#Quadratic Congruences

def is_quadratic_residue(a, n):
    # Check if a is a quadratic residue modulo n
    for x in range(n):
        if (x * x) % n == a % n:
            return True
    return False

# Example usage
a = 7
n = 11

is_residue = is_quadratic_residue(a, n)
print(f"{a} is a quadratic residue modulo {n}: {is_residue}")

