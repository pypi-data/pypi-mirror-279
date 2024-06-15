#Directed Elimination Ordering

import itertools


def directed_elimination_ordering(elements, relations):
    # Initialize the best solution to a large value
    best_violated = float('inf')
    best_solution = None

    # Define a function to calculate the number of violated edges of a solution
    def calculate_violated(solution):
        violated = 0
        for a, b in relations:
            if solution.index(a) > solution.index(b):
                violated += 1
        return violated

    # Define a function to perform the branch-and-bound search
    def search(elements, solution=[]):
        nonlocal best_violated, best_solution
        if not elements:
            violated = calculate_violated(solution)
            if violated < best_violated:
                best_violated = violated
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

print(directed_elimination_ordering(elements, relations))
