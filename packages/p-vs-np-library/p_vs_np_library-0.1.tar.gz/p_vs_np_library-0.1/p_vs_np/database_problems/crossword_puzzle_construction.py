#Crossword Puzzle Construction

def solve_crossword(grid, words):
    # Solve the crossword puzzle

    # Base case: all words have been placed
    if len(words) == 0:
        return grid

    word = words[0]

    # Try to place the word horizontally
    for i in range(len(grid)):
        for j in range(len(grid[0]) - len(word) + 1):
            if can_place_word(grid, word, i, j, "horizontal"):
                place_word(grid, word, i, j, "horizontal")
                result = solve_crossword(grid, words[1:])
                if result is not None:
                    return result
                remove_word(grid, word, i, j, "horizontal")

    # Try to place the word vertically
    for i in range(len(grid) - len(word) + 1):
        for j in range(len(grid[0])):
            if can_place_word(grid, word, i, j, "vertical"):
                place_word(grid, word, i, j, "vertical")
                result = solve_crossword(grid, words[1:])
                if result is not None:
                    return result
                remove_word(grid, word, i, j, "vertical")

    return None  # No solution found


def can_place_word(grid, word, row, col, direction):
    # Check if it is possible to place the word at the given position and direction

    # Check for word length and overlapping constraints
    for i in range(len(word)):
        if direction == "horizontal":
            if grid[row][col + i] != '-' and grid[row][col + i] != word[i]:
                return False
        else:
            if grid[row + i][col] != '-' and grid[row + i][col] != word[i]:
                return False

    return True


def place_word(grid, word, row, col, direction):
    # Place the word at the given position and direction

    for i in range(len(word)):
        if direction == "horizontal":
            grid[row][col + i] = word[i]
        else:
            grid[row + i][col] = word[i]


def remove_word(grid, word, row, col, direction):
    # Remove the word from the given position and direction

    for i in range(len(word)):
        if direction == "horizontal":
            grid[row][col + i] = '-'
        else:
            grid[row + i][col] = '-'


# Example usage
grid = [
    ['-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-']
]

words = ["cat", "dog", "car", "rat"]

solution = solve_crossword(grid, words)

if solution is not None:
    print("Crossword puzzle solution:")
    for row in solution:
        print(" ".join(row))
else:
    print("No solution found.")
