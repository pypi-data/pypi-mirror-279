#Oriented Diameter

import numpy as np

# Define the directed graph
G = nx.DiGraph()

# Add edges and nodes to the graph
G.add_edges_from([(1,2), (2,3), (3,4)])

# Initialize the distance matrix
n = len(G.nodes())
dist = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        try:
            dist[i][j] = nx.shortest_path_length(G, i, j)
        except nx.NetworkXNoPath:
            dist[i][j] = float('inf')

# Use the Floyd-Warshall algorithm to find the oriented diameter
for k in range(n):
    for i in range(n):
        for j in range(n):
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

# Find the maximum length of any simple path
oriented_diameter = max(dist.max(axis=0))

# Print the result
print("The oriented diameter of the graph is: ", oriented_diameter)
