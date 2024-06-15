#Kernel

import itertools

# Define the graph
G = nx.Graph()

# Add edges and nodes to the graph
G.add_edges_from([(1,2), (2,3), (3,4)])

# Create the set of all subgraphs of G
subgraphs = [G.subgraph(c).copy() for c in itertools.combinations(G.nodes(), 2)]

# Initialize the kernel
kernel = None

# Check for kernel
for subgraph in subgraphs:
    is_kernel = True
    for vertex in G.nodes():
        if vertex not in subgraph.nodes():
            if not any(neighbor in subgraph.nodes() for neighbor in G.neighbors(vertex)):
                is_kernel = False
                break
    if is_kernel:
        kernel = subgraph
        break

# Print the result
if kernel:
    print("The graph has a kernel:", kernel.nodes())
else:
    print("The graph has no kernel.")
