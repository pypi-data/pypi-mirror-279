#Chinese Postman For Mixed Graphs

import networkx as nx

def chinese_postman_mixed(graph):
    odd_nodes = [node for node, degree in graph.degree() if degree % 2 != 0]
    if len(odd_nodes) == 0:
        return nx.eulerian_circuit(graph)

    min_weight = float('inf')
    min_path = None

    for start_node in odd_nodes:
        matching_graph = nx.Graph()
        for u in odd_nodes:
            for v in odd_nodes:
                if u != v:
                    matching_graph.add_edge(u, v, weight=nx.dijkstra_path_length(graph, u, v))

        matching = nx.max_weight_matching(matching_graph, maxcardinality=True)
        augmented_graph = graph.copy()
        for u, v in matching:
            augmented_graph.add_edge(u, v)

        try:
            path = nx.eulerian_circuit(augmented_graph)
            weight = sum(augmented_graph[u][v]['weight'] for u, v in path)
            if weight < min_weight:
                min_weight = weight
                min_path = path
        except nx.NetworkXError:
            continue

    return min_path

# Example usage:
graph = nx.MultiGraph()
graph.add_edge('A', 'B', weight=2)
graph.add_edge('A', 'C', weight=1)
graph.add_edge('B', 'C', weight=3)
graph.add_edge('B', 'D', weight=2)
graph.add_edge('C', 'D', weight=1)
graph.add_edge('D', 'A', weight=3)
graph.add_edge('D', 'E', weight=4)

path = chinese_postman_mixed(graph)
total_weight = sum(graph[u][v]['weight'] for u, v in path)
print("Chinese Postman Path:", path)
print("Total Weight:", total_weight)
