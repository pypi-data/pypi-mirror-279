#Bottleneck Travelling Salesman

import itertools
import math

def calculate_distance(points, perm):
    n = len(perm)
    distance = 0
    for i in range(n):
        u = perm[i]
        v = perm[(i + 1) % n]
        distance += math.dist(points[u], points[v])
    return distance

def bottleneck_tsp(points):
    n = len(points)
    indices = range(n)
    min_distance = math.inf
    min_permutation = None

    for perm in itertools.permutations(indices):
        distance = calculate_distance(points, perm)
        if distance < min_distance:
            min_distance = distance
            min_permutation = perm

    return min_permutation, min_distance

# Example usage:
points = [(0, 0), (1, 1), (2, 3), (4, 2)]
permutation, distance = bottleneck_tsp(points)
print("Bottleneck TSP permutation:", permutation)
print("Bottleneck TSP distance:", distance)
