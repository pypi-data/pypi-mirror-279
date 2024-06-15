#Subgraph Homeomorphism (for a fixed graph H)

import networkx as nx

def is_subgraph_homeomorphic(G, H):
    G_edges = set(G.edges)
    H_edges = set(H.edges)

    # Check if the edge set of H is a subset of the edge set of G
    if H_edges.issubset(G_edges):
        # Create a subgraph of G using the same nodes as H
        subgraph_nodes = set(H.nodes)
        subgraph = G.subgraph(subgraph_nodes)

        # Check if the subgraph is homeomorphic to H
        return nx.is_isomorphic(subgraph, H)

    return False

# Example usage
if __name__ == '__main__':
    # Example graphs
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 1), (1, 4), (4, 5), (5, 6)])

    H = nx.Graph()
    H.add_edges_from([(1, 2), (2, 3), (3, 1)])

    # Check if G contains a subgraph homeomorphic to H
    if is_subgraph_homeomorphic(G, H):
        print("G contains a subgraph homeomorphic to H.")
    else:
        print("G does not contain a subgraph homeomorphic to H.")


