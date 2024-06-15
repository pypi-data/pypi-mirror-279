#Exact Cover By 3-Sets (X3C)

def find_x3c_solution(universe, sets):
    solution = []

    def backtrack(cover):
        nonlocal solution

        if len(universe) == 0:
            solution = cover
            return True

        if len(sets) == 0:
            return False

        set_ = sets[0]

        if len(set_) > len(universe):
            return False

        for i, elem in enumerate(set_):
            if elem in universe:
                new_cover = cover + [set_]
                new_universe = universe - set_

                if backtrack(new_cover):
                    return True

                universe.add(elem)  # Undo the selection if the current set did not lead to a solution

        return False

    if backtrack([]):
        return solution
    else:
        return []

# Example usage:
universe = {1, 2, 3, 4, 5, 6, 7, 8, 9}
sets = [{1, 2, 3}, {4, 5, 6}, {7, 8, 9}]

solution = find_x3c_solution(universe, sets)

if solution:
    print("X3C Solution:", solution)
else:
    print("No solution found.")
