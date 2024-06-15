#Min-Sum Multicenter

import itertools
import networkx as nx

def calculate_min_sum_multicenter(graph):
    n = graph.number_of_nodes()
    min_sum = float('inf')

    # Generate all possible combinations of vertices
    for r in range(1, n + 1):
        for centers in itertools.combinations(graph.nodes, r):
            sum_distances = calculate_sum_distances(graph, centers)
            min_sum = min(min_sum, sum_distances)

    return min_sum

def calculate_sum_distances(graph, centers):
    sum_distances = 0

    for node in graph.nodes:
        min_distance = float('inf')
        for center in centers:
            distance = nx.shortest_path_length(graph, source=center, target=node)
            min_distance = min(min_distance, distance)
        sum_distances += min_distance

    return sum_distances

# Example usage:
graph = nx.Graph()
graph.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4)])

min_sum_multicenter = calculate_min_sum_multicenter(graph)

print("Min-Sum Multicenter:", min_sum_multicenter)

