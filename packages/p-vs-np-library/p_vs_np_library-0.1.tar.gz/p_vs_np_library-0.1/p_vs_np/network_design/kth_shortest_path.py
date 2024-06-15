#Kth Shortest Path

import networkx as nx

def has_kth_shortest_paths(graph, source, target, k, b):
    # Find all simple paths from source to target
    paths = nx.all_simple_paths(graph, source, target)

    # Count the number of paths with length B or less
    count = 0
    for path in paths:
        total_length = sum(graph[u][v]['weight'] for u, v in zip(path, path[1:]))
        if total_length <= b:
            count += 1
            if count >= k:
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
k = 2
b = 10

has_k_shortest = has_kth_shortest_paths(graph, source, target, k, b)
print("Has K or more distinct paths from {} to {} with total length {} or less: {}".format(source, target, b, has_k_shortest))
