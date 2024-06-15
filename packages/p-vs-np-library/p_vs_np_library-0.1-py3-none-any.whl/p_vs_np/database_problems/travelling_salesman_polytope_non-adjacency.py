#Travelling Salesman Polytope non - adjacency

import itertools


def is_non_adjacent(graph):
    n = len(graph)

    # Generate all possible pairs of non-adjacent vertices
    for pair in itertools.combinations(range(n), 2):
        u, v = pair
        if not graph[u][v]:
            # Found a pair of non-adjacent vertices
            return True

    # No pair of non-adjacent vertices found
    return False


# Example usage
graph = [
    [False, True, True, True],
    [True, False, True, True],
    [True, True, False, True],
    [True, True, True, False]
]

result = is_non_adjacent(graph)
print(f"Does the Travelling Salesman Polytope have non-adjacent vertices? {result}")

