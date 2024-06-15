#Chromatic Index

import networkx as nx

def chromatic_index(G, K):
    max_degree = max(dict(G.degree()).values())

    # Check if the chromatic index is K or less
    if max_degree <= K:
        return True

    return False

# Example usage
if __name__ == '__main__':
    # Example instance
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 1)])
    K = 2

    # Solve the "Chromatic Index" problem
    result = chromatic_index(G, K)

    # Print the result
    if result:
        print("Graph has chromatic index", K, "or less")
    else:
        print("Graph does not have chromatic index", K, "or less")

