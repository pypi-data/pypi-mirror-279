#Chordal Graph Completion

import networkx as nx
from itertools import combinations

def chordal_graph_completion(G, K):
    # Generate all possible subsets of additional edges
    edge_subsets = []
    for k in range(K + 1):
        edge_subsets.extend(combinations(list(combinations(G.nodes(), 2)), k))

    # Check if any edge subset forms a chordal graph completion
    for subset in edge_subsets:
        if is_chordal_completion(G, subset):
            return True

    return False

def is_chordal_completion(G, edge_subset):
    # Create a copy of the original graph
    completion_graph = G.copy()

    # Add the edges in the subset to the copy
    completion_graph.add_edges_from(edge_subset)

    # Check if the resulting graph is chordal
    return nx.is_chordal(completion_graph)

# Example usage
if __name__ == '__main__':
    # Example instance
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 1)])
    K = 1

    # Solve the "Chordal Graph Completion" problem
    result = chordal_graph_completion(G, K)

    # Print the result
    if result:
        print("Graph can be extended to a chordal graph with at most", K, "additional edges")
    else:
        print("Graph cannot be extended to a chordal graph with at most", K, "additional edges")

