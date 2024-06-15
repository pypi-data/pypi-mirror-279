#Weighted Diameter

import heapq

# Define the weighted graph
G = nx.Graph()

# Add edges and nodes to the graph
G.add_edges_from([(1,2,3), (2,3,2), (3,4,1)])

# Initialize the diameter
weighted_diameter = 0

# Iterate over all nodes in the graph
for node in G.nodes():
    # Use the Dijkstra's algorithm to find the shortest path from the current node
    dist, pred = nx.single_source_dijkstra(G, node)
    # Find the longest simple path
    diameter = max(dist.values())
    # Update the weighted diameter if needed
    if diameter > weighted_diameter:
        weighted_diameter = diameter

# Print the result
print("The weighted diameter of the graph is: ", weighted_diameter)
