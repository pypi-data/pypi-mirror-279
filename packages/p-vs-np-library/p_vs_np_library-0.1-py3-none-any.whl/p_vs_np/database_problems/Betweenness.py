#Betweenness

import networkx as nx

def calculate_betweenness(graph):
    betweenness = nx.betweenness_centrality(graph)
    return betweenness

# Example usage
graph = nx.Graph()
graph.add_edges_from([(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)])

betweenness = calculate_betweenness(graph)
print("Betweenness centrality:")
for node, value in betweenness.items():
    print(f"Node {node}: {value}")
