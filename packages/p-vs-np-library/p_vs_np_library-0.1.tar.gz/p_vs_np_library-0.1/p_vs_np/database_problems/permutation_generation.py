#Permutation Generation

from itertools import permutations

def generate_permutations(elements):
    return list(permutations(elements))

# Example usage
elements = [1, 2, 3]
permutations = generate_permutations(elements)

print("Permutations:")
for perm in permutations:
    print(perm)

