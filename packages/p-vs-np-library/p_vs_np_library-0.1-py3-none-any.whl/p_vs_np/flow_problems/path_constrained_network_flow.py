#Path Constrained Network Flow

import networkx as nx
from itertools import combinations

def has_path_constrained_flow(graph, source, sink, path_constraints):
    # Create a new graph with auxiliary nodes for the path constraints
    augmented_graph = graph.copy()

    # Add auxiliary nodes and edges to represent the path constraints
    for constraint in path_constraints:
        auxiliary_node = 'AUX_' + '_'.join(constraint)
        augmented_graph.add_node(auxiliary_node)
        for u, v in combinations(constraint, 2):
            augmented_graph.add_edge(u, auxiliary_node, capacity=float('inf'))
            augmented_graph.add_edge(auxiliary_node, v, capacity=float('inf'))

    # Add auxiliary edges from source to the first nodes of the path constraints
    for constraint in path_constraints:
        augmented_graph.add_edge(source, constraint[0], capacity=float('inf'))

    # Add auxiliary edges from the last nodes of the path constraints to the sink
    for constraint in path_constraints:
        augmented_graph.add_edge(constraint[-1], sink, capacity=float('inf'))

    # Find the maximum flow in the augmented graph
    flow_value, flow_dict = nx.maximum_flow(augmented_graph, source, sink)

    # Check if the flow satisfies the path constraints
    for constraint in path_constraints:
        auxiliary_node = 'AUX_' + '_'.join(constraint)
        if flow_dict[source][constraint[0]] != 1 or flow_dict[constraint[-1]][sink] != 1 or flow_dict[auxiliary_node][constraint[0]] != 1:
            return False

    return True

# Example usage:
graph = nx.DiGraph()

# Add edges with capacities
graph.add_edge('A', 'B', capacity=5)
graph.add_edge('A', 'C', capacity=3)
graph.add_edge('B', 'C', capacity=2)
graph.add_edge('B', 'D', capacity=4)
graph.add_edge('C', 'D', capacity=3)

source = 'A'
sink = 'D'
path_constraints = [['A', 'B', 'D'], ['A', 'C', 'D']]

has_path_flow = has_path_constrained_flow(graph, source, sink, path_constraints)

print("Has feasible flow satisfying the path constraints:", has_path_flow)

