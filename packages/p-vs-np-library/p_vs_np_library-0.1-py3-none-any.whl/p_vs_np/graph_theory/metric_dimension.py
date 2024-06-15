#Metric Dimension

import itertools

# Define the graph
G = nx.Graph()

# Add edges and nodes to the graph
G.add_edges_from([(1,2), (2,3), (3,4)])

# Create all possible subsets
possible_subsets = [set(c) for c in itertools.combinations(G.nodes(), 2)]

# Check for metric dimension
for subset in possible_subsets:
    is_resolving = True
    for v, u in itertools.combinations(G.nodes(), 2):
        v_distances = {n: nx.shortest_path_length(G, v, n) for n in subset}
        u_distances = {n: nx.shortest_path_length(G, u, n) for n in subset}
        if v_distances == u_distances:
            is_resolving = False
            break
    if is_resolving:
        print("The subset", subset, "is a resolving set")
        break
else:
    print("The graph does not have a resolving set.")
