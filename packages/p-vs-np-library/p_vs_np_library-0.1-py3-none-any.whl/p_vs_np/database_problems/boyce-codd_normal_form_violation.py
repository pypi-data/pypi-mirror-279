#Boyce-Codd Normal Form Violation

def is_bcnf_violation(F, R):
    for X, Y in F:
        closure = compute_closure(X, F)
        if not closure.issubset(R):
            return True
    return False

def compute_closure(X, F):
    closure = set(X)
    updated = True

    while updated:
        updated = False
        for B, C in F:
            if B.issubset(closure) and not C.issubset(closure):
                closure.update(C)
                updated = True

    return closure

# Example usage
R = ['A', 'B', 'C', 'D']
F = [({'A'}, {'B'}), ({'B', 'C'}, {'D'})]

result = is_bcnf_violation(F, R)
if result:
    print("BCNF violation detected.")
else:
    print("No BCNF violation.")
