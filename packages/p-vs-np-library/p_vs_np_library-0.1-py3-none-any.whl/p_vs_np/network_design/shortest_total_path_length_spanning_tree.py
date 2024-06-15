#Shortest Total Path Length Spanning Tree

from collections import defaultdict
import heapq

def prim(n, edges):
    # initialize the graph
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))

    # initialize the tree
    tree = []

    # initialize the priority queue
    queue = [(0, 0, -1)]

    # initialize the visited set
    visited = set()

    # loop until the queue is empty
    while queue:
        # get the next vertex
        w, u, p = heapq.heappop(queue)

        # check if the vertex has been visited
        if u in visited:
            continue

        # add the vertex to the visited set
        visited.add(u)

        # add the edge to the tree
        if p != -1:
            tree.append((p, u, w))

        # add the adjacent vertices to the queue
        for v, w in graph[u]:
            if v not in visited:
                heapq.heappush(queue, (w, v, u))

    return tree
