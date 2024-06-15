#Max Cut

import itertools

def max_cut(graph):
    n = len(graph)
    max_cut_size = 0

    for mask in range(1 << n):
        cut_size = 0
        for u in range(n):
            for v in range(u+1, n):
                if ((mask >> u) & 1) != ((mask >> v) & 1):
                    cut_size += graph[u][v]
        max_cut_size = max(max_cut_size, cut_size)

    return max_cut_size

# Example usage:
graph = [
    [0, 1, 1, 0],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [0, 1, 1, 0]
]
result = max_cut(graph)
print("Maximum cut size:", result)
