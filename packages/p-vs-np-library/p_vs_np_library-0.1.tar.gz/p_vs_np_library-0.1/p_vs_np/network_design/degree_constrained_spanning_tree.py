#Degree Constrained Spanning Tree

from collections import defaultdict

def degree_constrained_spanning_tree(n, edges, degree_constraints):
    # initialize the graph
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # initialize the degree constraints
    degrees = {v: degree_constraints[v] for v in graph}

    # initialize the tree
    tree = []

    # initialize the queue
    queue = list(graph.keys())

    # loop until the queue is empty
    while queue:
        # get the next vertex
        v = queue.pop(0)

        # check if the vertex can be added to the tree
        if degrees[v] > 0:
            # update the degrees of the adjacent vertices
            for neighbor in graph[v]:
                degrees[neighbor] -= 1

            # add the vertex to the tree
            tree.append((v, neighbor))

            # update the queue
            queue.append(neighbor)

    return tree
