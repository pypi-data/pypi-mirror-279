##Graph Grundy Numbering

from collections import defaultdict

# Define the graph
G = nx.Graph()

# Add edges and nodes to the graph
G.add_edges_from([(1,2), (2,3), (3,4)])

# Define the maximum number of colors
max_colors = 3

# Initialize the grundy numbers
grundy = defaultdict(int)

# Define the backtracking function
def backtrack(v, c):
    if v not in grundy:
        # Assign the smallest available grundy number
        used_colors = set()
        for neighbor in G[v]:
            if neighbor in grundy:
                used_colors.add(grundy[neighbor])
        for color in range(max_colors):
            if color not in used_colors:
                grundy[v] = color
                break
    return grundy[v]

# Assign the grundy numbers
for v in G.nodes():
    backtrack(v, max_colors)

# Print the result
print("Grundy Numbers:", grundy)
