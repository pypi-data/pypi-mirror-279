#Numerical 3-Dimensional Matching

def can_numerical_3dm(A, B, C):
    target_sum = sum(A) // 3

    if sum(A) != sum(B) or sum(A) != sum(C):
        return False

    return numerical_3dm(A, B, C, [], [], [], target_sum)

def numerical_3dm(A, B, C, set_a, set_b, set_c, target_sum):
    if len(set_a) == len(set_b) == len(set_c) == target_sum:
        return True

    for i in range(len(A)):
        if A[i] in set_a or B[i] in set_b or C[i] in set_c:
            continue

        set_a.append(A[i])
        set_b.append(B[i])
        set_c.append(C[i])

        if numerical_3dm(A, B, C, set_a, set_b, set_c, target_sum):
            return True

        set_a.pop()
        set_b.pop()
        set_c.pop()

    return False

# Example usage:
A = [1, 2, 3, 4, 5]
B = [6, 7, 8, 9, 10]
C = [11, 12, 13, 14, 15]

result = can_numerical_3dm(A, B, C)

if result:
    print("There exists a Numerical 3-Dimensional Matching")
else:
    print("There does not exist a Numerical 3-Dimensional Matching")
