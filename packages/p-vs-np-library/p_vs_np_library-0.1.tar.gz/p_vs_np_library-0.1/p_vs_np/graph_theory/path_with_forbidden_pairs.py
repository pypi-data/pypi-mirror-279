#Path with Forbidden Pairs

import itertools

# Define the graph
G = nx.Graph()

# Add edges and nodes to the graph
G.add_edges_from([(1,2), (2,3), (3,4), (4,5)])

# Define the start vertex, end vertex, and forbidden pairs
start = 1
end = 5
forbidden = [(1,3), (3,5)]

# Initialize the path
path = [start]

# Find a path that avoids any edge in forbidden
def find_path(G, path, end, forbidden):
    if path[-1] == end:
        return path
    for neighbor in G[path[-1]]:
        if (path[-1], neighbor) not in forbidden and neighbor not in path:
            new_path = path + [neighbor]
            result = find_path(G, new_path, end, forbidden)
            if result:
                return result
    return None

result = find_path(G, path, end, forbidden)

# Print the result
if result:
    print("There exists a path from {} to {} that avoids any edge in {}".format(start, end, forbidden))
    print("Path: ", result)
else:
    print("There is no path from {} to {} that avoids any edge in {}.".format(start, end, forbidden))
