#Consecutive Ones Matrix Augmentation

def consecutive_ones_matrix_augmentation(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    def backtrack(row, col):
        if row == rows:
            return True

        if col == cols:
            return backtrack(row + 1, 0)

        if matrix[row][col] == 0:
            if can_place_one(row, col):
                matrix[row][col] = 1
                if backtrack(row, col + 1):
                    return True
                matrix[row][col] = 0

        return backtrack(row, col + 1)

    def can_place_one(row, col):
        for r in range(row + 1):
            if matrix[r][col] != 1:
                return False
        for c in range(col + 1):
            if matrix[row][c] != 1:
                return False
        return True

    return backtrack(0, 0)

# Example usage
matrix = [
    [1, 1, 0],
    [1, 0, 1],
    [0, 1, 1]
]

can_augment = consecutive_ones_matrix_augmentation(matrix)
if can_augment:
    print("Matrix can be augmented to have consecutive ones.")
else:
    print("Matrix cannot be augmented to have consecutive ones.")
