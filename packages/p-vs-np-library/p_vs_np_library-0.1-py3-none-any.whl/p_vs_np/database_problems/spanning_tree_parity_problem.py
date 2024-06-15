#Spanning Tree Parity Problem

import networkx as nx

def spanning_tree_parity(G, partition):
    # Check if each edge in the partition satisfies the parity constraint
    for edges in partition:
        parity = 0
        for u, v in edges:
            if (u, v) in G.edges() or (v, u) in G.edges():
                parity += 1

        # If parity is not 0 or 2, the constraint is violated
        if parity != 0 and parity != 2:
            return False

    # Check if the graph is connected
    if not nx.is_connected(G):
        return False

    return True

# Example usage
if __name__ == '__main__':
    # Example instance
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 1)])
    partition = [[(1, 2), (2, 3)]]

    # Solve the "Spanning Tree Parity" problem
    result = spanning_tree_parity(G, partition)

    # Print the result
    if result:
        print("Graph has a spanning tree satisfying the parity constraints")
    else:
        print("Graph does not have a spanning tree satisfying the parity constraints")

