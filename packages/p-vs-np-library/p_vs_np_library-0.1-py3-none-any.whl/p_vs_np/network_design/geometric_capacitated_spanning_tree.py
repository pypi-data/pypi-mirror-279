#geometric capacitated spanning tree

import numpy as np

def geometric_capacitated_spanning_tree(n, coordinates, capacity):
    # Initialize the tree
    tree = []
    total_weight = 0
    visited = set()
    visited.add(0)
    current = 0
    while len(visited) < n:
        # Find the closest vertex to the current vertex
        closest = None
        closest_distance = float("inf")
        for i in range(n):
            if i not in visited:
                d = np.linalg.norm(coordinates[i] - coordinates[current])
                if d < closest_distance:
                    closest = i
                    closest_distance = d
        # Check if adding the edge to the tree exceeds the capacity
        if closest_distance + total_weight <= capacity:
            tree.append((current, closest, closest_distance))
            total_weight += closest_distance
            visited.add(closest)
            current = closest
        else:
            break
    return tree
