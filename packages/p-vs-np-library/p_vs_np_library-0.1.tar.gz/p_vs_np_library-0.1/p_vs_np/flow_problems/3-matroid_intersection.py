#3-Matroid Intersection

def has_3_matroid_intersection(matroid1, matroid2, matroid3):
    universe = set.union(matroid1, matroid2, matroid3)

    for element in universe:
        if element in matroid1 and element in matroid2 and element in matroid3:
            return True

    return False

# Example usage:
matroid1 = {1, 2, 3, 4}
matroid2 = {3, 4, 5, 6}
matroid3 = {2, 3, 4, 5}

result = has_3_matroid_intersection(matroid1, matroid2, matroid3)

if result:
    print("3-Matroid intersection exists")
else:
    print("3-Matroid intersection does not exist")
