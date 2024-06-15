#Consecutive ones submatrix

def consecutive_ones_submatrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    submatrix = []

    def backtrack(row, submatrix):
        if row == rows:
            return submatrix

        for i in range(cols):
            if is_valid(submatrix, row, i):
                submatrix.append(i)
                result = backtrack(row + 1, submatrix)
                if result:
                    return result
                submatrix.pop()

    return backtrack(0, submatrix)

def is_valid(submatrix, row, col):
    for r, c in enumerate(submatrix):
        if row == r or col == c or abs(row - r) == abs(col - c):
            return False
    return True

# Example usage
matrix = [
    [1, 0, 1, 1],
    [1, 1, 1, 0],
    [0, 1, 1, 1]
]

result = consecutive_ones_submatrix(matrix)
if result:
    print("Consecutive Ones Submatrix: ", result)
else:
    print("No Consecutive Ones Submatrix found.")
