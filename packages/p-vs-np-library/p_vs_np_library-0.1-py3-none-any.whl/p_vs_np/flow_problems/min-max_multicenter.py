#Min-Max Multicenter


import itertools
import networkx as nx

def calculate_min_max_multicenter(graph):
    n = graph.number_of_nodes()
    min_radius = float('inf')

    # Generate all possible combinations of vertices
    for r in range(1, n + 1):
        for centers in itertools.combinations(graph.nodes, r):
            radius = calculate_radius(graph, centers)
            min_radius = min(min_radius, radius)

    return min_radius

def calculate_radius(graph, centers):
    max_distance = 0

    for node in graph.nodes:
        min_distance = float('inf')
        for center in centers:
            distance = nx.shortest_path_length(graph, source=center, target=node)
            min_distance = min(min_distance, distance)
        max_distance = max(max_distance, min_distance)

    return max_distance

# Example usage:
graph = nx.Graph()
graph.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4)])

min_max_multicenter_radius = calculate_min_max_multicenter(graph)

print("Min-Max Multicenter Radius:", min_max_multicenter_radius)
