#Comparative Containment

def is_comparative_containment(subsets):
    n = len(subsets)

    for i in range(n):
        for j in range(n):
            if i != j:
                if not is_subset(subsets[i], subsets[j]):
                    return False

    return True

def is_subset(set1, set2):
    return set1.issubset(set2)

# Example usage:
subsets = [
    {1, 2},
    {1, 2, 3},
    {2, 3}
]

result = is_comparative_containment(subsets)

if result:
    print("Comparative containment exists")
else:
    print("Comparative containment does not exist")

