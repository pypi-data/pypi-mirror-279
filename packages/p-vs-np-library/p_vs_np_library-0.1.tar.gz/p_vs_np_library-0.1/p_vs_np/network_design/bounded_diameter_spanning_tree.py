#Bounded Diameter Spanning Tree

from collections import defaultdict
import heapq

def find_diameter(graph, source):
    # initialize the visited set
    visited = set()

    # initialize the queue
    queue = [(source, 0)]

    # loop until the queue is empty
    while queue:
        # get the next vertex
        v, d = queue.pop(0)

        # check if the vertex has been visited
        if v in visited:
            continue

        # add the vertex to the visited set
        visited.add(v)

        # add the adjacent vertices to the queue
        for neighbor in graph[v]:
            queue.append((neighbor, d + 1))

    # return the vertex and its distance from the source
    return v, d

def bounded_diameter_spanning_tree(n, edges, bound):
    # find the minimum spanning tree
    mst = kruskal(n, edges)

    # find the diameter of the minimum spanning tree
    graph = defaultdict(list)
    for u, v, w in mst:
        graph[u].append(v)
        graph[v].append(u)
    end1, diameter = find_diameter(graph, 0)
    end2, _ = find_diameter(graph, end1)

    # remove edges from the tree until the diameter is less than the bound
    while diameter > bound:
        for i in range(len(mst)):
            u, v, w = mst[i]
            if (u == end1 and v == end2) or (u == end2 and v == end1):
                del mst[i]
                break
        graph = defaultdict(list)
        for u, v, w in mst:
            graph[u].append(v)
            graph[v].append(u)
        end1, diameter = find_diameter(graph, 0)
        end2, _ = find_diameter(graph, end1)

    return mst
