#Minimum Cut Linear Arrangement

import itertools


def minimum_cut_linear_arrangement(elements, relations, cost_matrix):
    # Initialize the best solution to a large value
    best_cuts = float('inf')
    best_solution = None

    # Define a function to calculate the number of cuts of a solution
    def calculate_cuts(solution):
        cuts = 0
        for a, b in relations:
            if solution.index(a) > solution.index(b):
                cuts += 1
        return cuts

    # Define a function to perform the branch-and-bound search
    def search(elements, solution=[]):
        nonlocal best_cuts, best_solution
        if not elements:
            cuts = calculate_cuts(solution)
            if cuts < best_cuts:
                best_cuts = cuts
                best_solution = solution
        else:
            # Use a heuristic function to order the elements
            # in the next level of the search tree
            heuristic = lambda e: sum(1 for a, b in relations if e == a and solution[-1] == b)
            for e in sorted(elements, key=heuristic):
                search(elements - {e}, solution + [e])

    # Perform the branch-and-bound search
    search(set(elements))

    # Return the best solution
    return best_solution


# Example usage
elements = [1, 2, 3, 4]
relations = [(1, 2), (3, 4)]
cost_matrix = [[0, 10, 15, 20],
               [10, 0, 35, 25],
               [15, 35, 0, 30],
               [20, 25, 30, 0]]

print(minimum_cut_linear_arrangement(elements, relations, cost_matrix))
