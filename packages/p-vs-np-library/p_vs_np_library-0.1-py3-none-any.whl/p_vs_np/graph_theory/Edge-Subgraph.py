#Edge-Subgraph

from itertools import combinations

def edge_subgraph(graph):
    max_subgraph = []
    for vertex in graph:
        for subset in combinations(graph.edges(), vertex):
            subgraph = nx.Graph()
            subgraph.add_edges_from(subset)
            if nx.is_connected(subgraph):
                if len(subset) > len(max_subgraph):
                    max_subgraph = subset
    return max_subgraph

graph = nx.Graph()
graph.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)])

subgraph = edge_subgraph(graph)

print(subgraph)
