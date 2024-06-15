#Set Basis

def set_basis(sets):
    universe = set.union(*sets)
    covered_elements = set()
    basis = []

    while len(covered_elements) < len(universe):
        max_covered_count = 0
        max_covered_set = None

        for set_ in sets:
            covered_count = len(set_.difference(covered_elements))

            if covered_count > max_covered_count:
                max_covered_count = covered_count
                max_covered_set = set_

        if max_covered_set is None:
            break

        basis.append(max_covered_set)
        covered_elements.update(max_covered_set)

    return basis

# Example usage:
sets = [
    {1, 2, 3},
    {2, 3, 4},
    {3, 4, 5},
    {4, 5, 6}
]

basis = set_basis(sets)

print("Set Basis:")
for set_ in basis:
    print(set_)
