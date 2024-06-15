##Planar Subgraph

import networkx as nx

def planar_subgraph(graph):
    max_subgraph = []
    for vertex in graph:
        for subset in combinations(graph, vertex):
            subgraph = graph.subgraph(subset)
            if nx.check_planarity(subgraph)[0]:
                if len(subset) > len(max_subgraph):
                    max_subgraph = subset
    return max_subgraph

graph = nx.Graph()
graph.add_edges_from([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])

subgraph = planar_subgraph(graph)

print(subgraph)
