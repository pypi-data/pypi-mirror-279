#Alternating Hitting Set


def is_hitting_set(C, H):
    for s in C:
        if len(set(s) & set(H)) % 2 == 0:
            return False
    return True


def find_alternating_hitting_set(C, k):
    n = len(C)
    elements = set()
    for s in C:
        elements.update(s)

    # Try all possible combinations of size at most k
    for i in range(1, k + 1):
        for subset in itertools.combinations(elements, i):
            H = list(subset)
            if is_hitting_set(C, H):
                return H

    return None


# Example usage
C = [['A', 'B', 'C'], ['B', 'D'], ['A', 'C', 'D'], ['B', 'D', 'E']]
k = 3

hitting_set = find_alternating_hitting_set(C, k)
if hitting_set is not None:
    print("Found hitting set:", hitting_set)
else:
    print("No hitting set of size at most", k, "found.")
