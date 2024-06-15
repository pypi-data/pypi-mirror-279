#Additional Key

def has_additional_key(R, K, F):
    # Check if each subset of R not in K is a key
    for subset in powerset(R):
        if subset not in K:
            if is_key(subset, R, F):
                return True

    return False

def is_key(subset, R, F):
    closure = set(subset)
    updated = True

    while updated:
        updated = False
        for B, C in F:
            if B.issubset(closure) and not C.issubset(closure):
                closure.update(C)
                updated = True

    return closure == set(R)

def powerset(s):
    powerset = [[]]
    for elem in s:
        powerset.extend([subset + [elem] for subset in powerset])
    return powerset

# Example usage
R = ['A', 'B', 'C']
K = [{'A'}, {'B'}]
F = [({'A'}, {'B'}), ({'B'}, {'C'})]

result = has_additional_key(R, K, F)
if result:
    print("There exists an additional key.")
else:
    print("No additional key exists.")
