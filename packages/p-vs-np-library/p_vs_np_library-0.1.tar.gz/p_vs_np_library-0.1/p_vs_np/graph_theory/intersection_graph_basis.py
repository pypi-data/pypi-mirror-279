#Intersection Graph Basis

import itertools

# Define the graph
G = nx.Graph()

# Add edges and nodes to the graph
G.add_edges_from([(1,2), (2,3), (3,4)])

# Create all possible sets
possible_sets = [set(c) for c in itertools.combinations(G.nodes(), 2)]

# Check for intersection graph basis
for sets in possible_sets:
    is_basis = True
    for edge in G.edges():
        if set(edge) not in sets:
            is_basis = False
            break
    if is_basis:
        print("The graph is an intersection graph of the sets", sets)
        break
else:
    print("The graph can not be represented as an intersection graph.")

