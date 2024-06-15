#Graph Contractibility

import itertools

# Define the graph
G = nx.Graph()

# Add edges and nodes to the graph
G.add_edges_from([(1,2), (2,3), (3,4)])

# Define the number of steps
k = 2

# Create the set of all subgraphs of G
subgraphs = [G.subgraph(c).copy() for c in itertools.combinations(G.nodes(), 2)]

# Initialize the step count
step_count = 0

# Check if the graph can be contracted to a single node in k steps
while len(G.nodes()) > 1:
    step_count += 1
    if step_count > k:
        print("The graph cannot be contracted to a single node in {} steps.".format(k))
        break
    edge = G.edges()[0]
    G.remove_nodes_from(edge)
    G = nx.contracted_nodes(G, edge[0], edge[1])

# Print the result
if step_count <= k:
    print("The graph can be contracted to a single node in {} steps.".format(step_count))

