#Simply Deviated Disjunction

from itertools import chain, combinations

def simply_deviated_disjunction(M):
    m = len(M[0])  # Number of elements in each tuple
    n = len(M)     # Number of tuples

    # Generate all possible partitions of {1, 2, ..., m}
    partitions = generate_partitions(m)

    # Iterate over all partitions
    for I, J in partitions:
        # Iterate over all possible assignments
        for assignment in product([0, 1], repeat=m):
            phi_true_and_psi_true = 0
            phi_true_and_psi_false = 0
            phi_false_and_psi_true = 0
            phi_false_and_psi_false = 0

            # Iterate over each tuple in M
            for t in M:
                phi = all(t[j] == assignment[j] for j in I)
                psi = all(t[j] == assignment[j] for j in J)

                if phi and psi:
                    phi_true_and_psi_true += 1
                elif phi and not psi:
                    phi_true_and_psi_false += 1
                elif not phi and psi:
                    phi_false_and_psi_true += 1
                else:
                    phi_false_and_psi_false += 1

            # Check the simply deviated condition
            if (phi_true_and_psi_true * phi_false_and_psi_false) > (phi_true_and_psi_false * phi_false_and_psi_true):
                return True

    return False

def generate_partitions(m):
    # Generate all possible partitions of {1, 2, ..., m}
    partitions = []
    for i in range(1, m):
        for c in combinations(range(m), i):
            partitions.append((c, tuple(set(range(m)) - set(c))))
    return partitions

# Example usage
if __name__ == '__main__':
    # Example instance M
    M = [
        [1, 0, 1, 0],
        [0, 1, 1, 0],
        [1, 0, 0, 1]
    ]

    # Solve the "Simply Deviated Disjunction" problem
    result = simply_deviated_disjunction(M)

    # Print the result
    if result:
        print("There exists a partition and assignment that satisfy the simply deviated condition.")
    else:
        print("No partition and assignment satisfy the simply deviated condition.")
