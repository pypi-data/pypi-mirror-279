#Total Unimodularity

import numpy as np

def is_total_unimodular(matrix):
    # Convert matrix to numpy array
    M = np.array(matrix)

    # Check if all submatrices have determinants in the set (-1, 0, 1)
    for i in range(1, M.shape[0] + 1):
        for submatrix in get_submatrices(M, i):
            determinant = np.linalg.det(submatrix)
            if determinant not in (-1, 0, 1):
                return False

    return True

def get_submatrices(matrix, k):
    n = matrix.shape[0]
    for i in range(n - k + 1):
        for j in range(n - k + 1):
            yield matrix[i:i+k, j:j+k]

# Example usage
if __name__ == '__main__':
    # Example matrix
    matrix = [[1, 0, 1],
              [0, 1, 0],
              [1, 0, 1]]

    # Check if the matrix is totally unimodular
    result = is_total_unimodular(matrix)

    # Print the result
    if result:
        print("The matrix is totally unimodular.")
    else:
        print("The matrix is not totally unimodular.")
