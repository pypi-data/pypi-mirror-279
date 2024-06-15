#Shortest Weight-Constrained Path

import networkx as nx

def has_shortest_weight_constrained_path(graph, source, target, w, k):
    # Find all simple paths from source to target
    paths = nx.all_simple_paths(graph, source, target)

    # Check if any path satisfies the weight and length constraints
    for path in paths:
        total_weight = sum(graph[u][v]['weight'] for u, v in zip(path, path[1:]))
        total_length = len(path) - 1
        if total_weight <= w and total_length <= k:
            return True

    return False

# Example usage:
graph = nx.DiGraph()
graph.add_edge('A', 'B', weight=2)
graph.add_edge('B', 'C', weight=3)
graph.add_edge('C', 'D', weight=4)
graph.add_edge('D', 'A', weight=5)

source = 'A'
target = 'D'
w = 8
k = 3

has_shortest = has_shortest_weight_constrained_path(graph, source, target, w, k)
print("Has Shortest Weight-Constrained Path from {} to {} with total weight {} or less and total length {} or less: {}".format(source, target, w, k, has_shortest))

