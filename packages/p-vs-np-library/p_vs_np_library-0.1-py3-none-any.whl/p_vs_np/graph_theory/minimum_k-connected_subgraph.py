#Minimum K-Connected Subgraph

from itertools import combinations

def min_k_connected_subgraph(graph, k):
    min_subgraph = graph
    for vertex in graph:
        for subset in combinations(graph.nodes(), vertex):
            subgraph = graph.subgraph(subset)
            if nx.node_connectivity(subgraph) >= k:
                if len(subset) < len(min_subgraph):
                    min_subgraph = subgraph
    return min_subgraph

graph = nx.Graph()
graph.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)])

subgraph = min_k_connected_subgraph(graph, 2)

print(subgraph.edges())
