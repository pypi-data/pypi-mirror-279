#Disjoint Connecting Paths

import networkx as nx

def find_disjoint_connecting_paths(graph, source_nodes, target_nodes):
    # Create a new graph with a supersource and a supersink
    supergraph = nx.DiGraph()
    supergraph.add_node('s')
    supergraph.add_node('t')

    # Connect source nodes to supersource and target nodes to supersink
    for source in source_nodes:
        supergraph.add_edge('s', source, capacity=1)
    for target in target_nodes:
        supergraph.add_edge(target, 't', capacity=1)

    # Find maximum flow in the supergraph
    flow_value, flow_dict = nx.maximum_flow(supergraph, 's', 't')

    # Retrieve the disjoint connecting paths
    paths = []
    for source in source_nodes:
        for target in target_nodes:
            if flow_dict[source][target] == 1:
                path = nx.shortest_path(graph, source=source, target=target)
                paths.append(path)

    return paths

# Example usage:
graph = nx.DiGraph()

# Add edges to the graph
graph.add_edge('A', 'B')
graph.add_edge('A', 'C')
graph.add_edge('B', 'C')
graph.add_edge('B', 'D')
graph.add_edge('C', 'D')

# Define source and target nodes
source_nodes = ['A']
target_nodes = ['D']

# Find disjoint connecting paths
paths = find_disjoint_connecting_paths(graph, source_nodes, target_nodes)

# Print the paths
for path in paths:
    print("Path:", ' -> '.join(path))
