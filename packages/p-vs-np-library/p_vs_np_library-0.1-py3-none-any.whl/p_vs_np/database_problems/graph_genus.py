#Graph Genus

import networkx as nx
from itertools import combinations

def graph_genus(G, K):
    # Generate all possible subsets of edges of size K or less
    edge_subsets = []
    for k in range(K + 1):
        edge_subsets.extend(combinations(G.edges(), k))

    # Check if any edge subset forms a valid embedding
    for subset in edge_subsets:
        if is_valid_embedding(G, subset):
            return True

    return False

def is_valid_embedding(G, edge_subset):
    # Create a copy of the original graph
    embedded_graph = G.copy()

    # Remove the edges in the subset from the copy
    embedded_graph.remove_edges_from(edge_subset)

    # Check if the resulting graph is planar
    return nx.check_planarity(embedded_graph)[0]

# Example usage
if __name__ == '__main__':
    # Example instance
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 1), (3, 4), (4, 1)])
    K = 1

    # Solve the "Graph Genus" problem
    result = graph_genus(G, K)

    # Print the result
    if result:
        print("Graph can be embedded on a surface of genus", K)
    else:
        print("Graph cannot be embedded on a surface of genus", K)

