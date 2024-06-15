#Maximum Leaf Spanning Tree

from collections import defaultdict


def maximum_leaf_spanning_tree(n, edges):
    # initialize the graph
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # initialize the tree
    tree = []

    # initialize the queue
    queue = list(graph.keys())

    # loop until the queue is empty
    while queue:
        # get the leaf with maximum degree
        leaf = max(queue, key=lambda v: len(graph[v]))

        # find its neighbor
        neighbor = graph[leaf][0]

        # remove the leaf from the graph
        graph[neighbor].remove(leaf)
        queue.remove(leaf)

        # add the edge to the tree
        tree.append((leaf, neighbor))

    return tree
