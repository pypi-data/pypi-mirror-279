#K-Closure

import itertools

# Define the graph
G = nx.Graph()

# Add edges and nodes to the graph
G.add_edges_from([(1,2), (2,3), (3,4)])

# Define the value of k
k = 2

# Initialize the k-closure
k_closure = nx.Graph()

# Check for k-closure
for vertex in G.nodes():
    for neighbor in nx.single_source_shortest_path_length(G, vertex, k).keys():
        k_closure.add_edge(vertex, neighbor)

# Print the result
print("The k-closure of the graph is: ", k_closure.edges())
