#Permanent
Evaluation


def compute_permanent(matrix):
    n = len(matrix)
    cols = list(range(n))
    result = 0

    def inner_permanent(matrix, cols):
        nonlocal result
        if len(cols) == 1:
            result += matrix[0][cols[0]]
            return

        for col in cols:
            new_cols = cols[:]
            new_cols.remove(col)
            inner_permanent(matrix[1:], new_cols)

    inner_permanent(matrix, cols)
    return result


# Example usage
matrix = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]

permanent = compute_permanent(matrix)
print("The permanent of the matrix is:", permanent)

