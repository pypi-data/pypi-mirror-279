#Intersection Pattern

def has_intersection_pattern(sets):
    n = len(sets)

    for i in range(1 << n):
        pattern = set()

        for j in range(n):
            if i & (1 << j):
                pattern.update(sets[j])

        is_valid_pattern = True

        for k in range(n):
            if not any(element in sets[k] for element in pattern):
                is_valid_pattern = False
                break

        if is_valid_pattern:
            return True

    return False

# Example usage:
sets = [
    {1, 2, 3},
    {2, 3, 4},
    {3, 4, 5}
]

result = has_intersection_pattern(sets)

if result:
    print("Intersection pattern exists")
else:
    print("Intersection pattern does not exist")

