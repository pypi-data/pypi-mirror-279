#Matrix Domination

import itertools

def matrix_domination(M, K):
    n, m = len(M), len(M[0])

    # Get the indices of non-zero entries in the matrix
    non_zero_indices = [(i, j) for i in range(n) for j in range(m) if M[i][j] == 1]

    # Generate all possible subsets of at most K non-zero entries
    for subset_size in range(K+1):
        for subset in itertools.combinations(non_zero_indices, subset_size):
            # Check if the subset dominates all others
            if dominates_all(subset, M):
                return True

    return False

def dominates_all(subset, M):
    n, m = len(M), len(M[0])

    for i in range(n):
        for j in range(m):
            if M[i][j] == 1 and not any(i == p or j == q for p, q in subset):
                return False

    return True

# Example usage
if __name__ == '__main__':
    # Example matrix M
    M = [
        [1, 0, 0, 1],
        [0, 1, 1, 0],
        [1, 1, 0, 0],
        [1, 0, 0, 1]
    ]
    K = 4

    # Check if a dominating subset exists
    if matrix_domination(M, K):
        print("A dominating subset of at most", K, "non-zero entries exists.")
    else:
        print("No dominating subset of at most", K, "non-zero entries exists.")

