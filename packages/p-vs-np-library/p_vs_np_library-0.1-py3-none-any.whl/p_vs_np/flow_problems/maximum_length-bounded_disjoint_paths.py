#Maximum Length-Bounded Disjoint Paths

import networkx as nx

def find_maximum_length_bounded_disjoint_paths(graph, source, target, max_length):
    # Create a copy of the graph
    modified_graph = graph.copy()

    # Add a dummy node
    dummy_node = 'dummy'
    modified_graph.add_node(dummy_node)

    # Connect the dummy node to the target node
    for node in modified_graph.nodes():
        if node != target and node != dummy_node:
            modified_graph.add_edge(node, dummy_node, capacity=1)

    # Find the maximum flow from the source to the dummy node
    flow_value, flow_dict = nx.maximum_flow(modified_graph, source, dummy_node)

    # Find the paths based on the flow values
    paths = []
    for node in modified_graph.neighbors(dummy_node):
        if flow_dict[source][node] == 1:
            path = nx.shortest_path(graph, source=source, target=node)
            paths.append(path[:-1])  # Remove the dummy node from the path

    # Filter paths based on maximum length constraint
    filtered_paths = [path for path in paths if len(path) <= max_length]

    return filtered_paths

# Example usage:
graph = nx.DiGraph()

# Add edges to the graph
graph.add_edge('A', 'B')
graph.add_edge('A', 'C')
graph.add_edge('B', 'C')
graph.add_edge('B', 'D')
graph.add_edge('C', 'D')

# Define source and target nodes
source = 'A'
target = 'D'

# Define maximum length
max_length = 3

# Find maximum length-bounded disjoint paths
paths = find_maximum_length_bounded_disjoint_paths(graph, source, target, max_length)

# Print the paths
for path in paths:
    print("Path:", ' -> '.join(path))
