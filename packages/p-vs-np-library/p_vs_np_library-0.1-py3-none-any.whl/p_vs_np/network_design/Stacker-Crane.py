#Stacker-Crane

import networkx as nx

def directed_chinese_postman(graph, required_edges, bound):
    augmented_graph = graph.copy()

    # Add required edges with high weight
    for edge in required_edges:
        u, v, weight = edge
        augmented_graph.add_edge(u, v, weight=weight)

    # Find the Eulerian circuit in the augmented graph
    eulerian_circuit = nx.eulerian_circuit(augmented_graph)

    # Check if the circuit satisfies the constraints
    total_length = sum(augmented_graph[u][v]['weight'] for u, v in eulerian_circuit)
    if total_length <= bound:
        return eulerian_circuit
    else:
        return None

# Example usage:
graph = nx.DiGraph()
graph.add_edge('A', 'B', weight=2)
graph.add_edge('B', 'C', weight=3)
graph.add_edge('C', 'D', weight=4)
graph.add_edge('D', 'A', weight=5)
graph.add_edge('D', 'B', weight=1)

required_edges = [('A', 'B', 2), ('D', 'B', 1)]
bound = 12

path = directed_chinese_postman(graph, required_edges, bound)
if path is not None:
    total_length = sum(graph[u][v]['weight'] for u, v in path)
    print("Directed Chinese Postman Path:", path)
    print("Total Length:", total_length)
else:
    print("No feasible solution within the specified bound.")

