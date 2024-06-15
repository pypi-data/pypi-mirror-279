#Minimum Cover

def minimum_cover(universe, sets):
    covered_elements = set()
    minimum_cover = []

    while len(covered_elements) < len(universe):
        max_covered_count = 0
        max_covered_set = None

        for set_ in sets:
            covered_count = len(set_.intersection(universe - covered_elements))

            if covered_count > max_covered_count:
                max_covered_count = covered_count
                max_covered_set = set_

        if max_covered_set is None:
            break

        minimum_cover.append(max_covered_set)
        covered_elements.update(max_covered_set)

    return minimum_cover

# Example usage:
universe = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
sets = [
    {1, 2, 3, 4},
    {3, 4, 5, 6},
    {5, 6, 7, 8},
    {7, 8, 9, 10}
]

cover = minimum_cover(universe, sets)

print("Minimum Cover:")
for set_ in cover:
    print(set_)
