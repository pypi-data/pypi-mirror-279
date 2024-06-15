#Path Distinguishers

import itertools

# Define the graph
G = nx.Graph()

# Add edges and nodes to the graph
G.add_edges_from([(1,2), (2,3), (3,4)])

# Create all possible paths
possible_paths = [list(nx.all_simple_paths(G,i,j)) for i,j in itertools.combinations(G.nodes(), 2)]
possible_paths = [path for sublist in possible_paths for path in sublist]

# Check for Path Distinguishers
for path_set in possible_paths:
    is_distinguisher = True
    for path in path_set:
        for v, u in itertools.combinations(path, 2):
            if path[0] == u and path[-1] == v:
                is_distinguisher = False
                break
        if not is_distinguisher:
            break
    if is_distinguisher:
        print("The set of paths", path_set, "is a set of Path Distinguishers")
        break
else:
    print("The graph does not have a set of Path Distinguishers.")

