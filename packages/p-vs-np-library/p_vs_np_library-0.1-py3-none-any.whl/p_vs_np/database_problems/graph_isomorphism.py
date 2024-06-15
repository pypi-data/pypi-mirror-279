#Graph Isomorphism

import networkx as nx

def is_graph_isomorphic(graph1, graph2):
    return nx.is_isomorphic(graph1, graph2)

# Example usage
if __name__ == '__main__':
    # Example graphs
    graph1 = nx.Graph()
    graph1.add_edges_from([(1, 2), (2, 3), (3, 1)])

    graph2 = nx.Graph()
    graph2.add_edges_from([(4, 5), (5, 6), (6, 4)])

    # Check if the graphs are isomorphic
    if is_graph_isomorphic(graph1, graph2):
        print("The graphs are isomorphic.")
    else:
        print("The graphs are not isomorphic.")
