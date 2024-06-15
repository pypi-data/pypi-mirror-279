#Matrix Cover

def matrix_cover(matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    # Initialize a list to track the covered columns
    covered_cols = [False] * num_cols

    # Iterate over the rows, selecting the row that covers the maximum number of uncovered columns at each step
    while not all(covered_cols):
        max_covered_count = 0
        max_covered_row = None

        for row in range(num_rows):
            if not all(matrix[row][col] or covered_cols[col] for col in range(num_cols)):
                # Count the number of uncovered columns for this row
                covered_count = sum(not matrix[row][col] and not covered_cols[col] for col in range(num_cols))

                if covered_count > max_covered_count:
                    max_covered_count = covered_count
                    max_covered_row = row

        # If there is a row that covers at least one uncovered column, mark those columns as covered
        if max_covered_row is not None:
            for col in range(num_cols):
                if not matrix[max_covered_row][col]:
                    covered_cols[col] = True

    # Find the indices of the covered columns
    covered_indices = [index for index, covered in enumerate(covered_cols) if covered]

    return covered_indices

# Example usage
if __name__ == '__main__':
    # Example matrix
    matrix = [
        [1, 0, 1, 0, 0],
        [1, 1, 0, 0, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 0, 1, 1]
    ]

    # Solve the matrix cover problem
    covered_indices = matrix_cover(matrix)

    # Print the result
    print("Covered Columns:", covered_indices)

