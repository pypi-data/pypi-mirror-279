#K^TH Best Spanning Tree

from collections import defaultdict
from heapq import heappush, heappop

def k_best_spanning_tree(n, edges, k):
    def kruskal():
        edges.sort(key=lambda x: x[2])
        tree = []
        for u, v, w in edges:
            if find(u) != find(v):
                union(u, v)
                tree.append((u, v, w))
                if len(tree) == n - 1:
                    return tree
        return tree

    def find(u):
        if parents[u] != u:
            parents[u] = find(parents[u])
        return parents[u]

    def union(u, v):
        parents[find(u)] = find(v)

    k_best_trees = []
    parents = {i: i for i in range(n)}
    for _ in range(k):
        tree = kruskal()
        k_best_trees.append(tree)
        for u, v, _ in tree:
            parents[u] = u
            parents[v] = v
    return k_best_trees
