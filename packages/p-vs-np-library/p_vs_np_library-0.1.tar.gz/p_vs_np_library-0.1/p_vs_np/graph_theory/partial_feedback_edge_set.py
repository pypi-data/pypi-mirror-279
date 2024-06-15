#Partial Feedback Edge Set

import networkx as nx


def partial_feedback_edge_set(graph, k):
    def dfs(v, visited, adj_list):
        visited.add(v)
        for neighbor in adj_list[v]:
            if neighbor not in visited:
                dfs(neighbor, visited, adj_list)

    def is_acyclic(graph):
        visited = set()
        for vertex in range(len(graph)):
            if vertex not in visited:
                stack = [vertex]
                while stack:
                    v = stack.pop()
                    if v not in visited:
                        visited.add(v)
                        stack.extend(graph[v])
                    elif v in stack:
                        return False
        return True

    def k_edges(graph, k):
        edges = nx.minimum_spanning_edges(nx.from_numpy_matrix(graph), algorithm='kruskal', data=False)
        edges = set(edges)
        edges_to_remove = set()
        for edge in edges:
            edges_to_remove.add(edge)
            if len(edges_to_remove) == k:
                if is_acyclic(graph):
                    return edges_to_remove
                else:
                    edges_to_remove.remove(edge)

    return k_edges(graph, k)


graph = [[0, 1, 1, 0],
         [1, 0, 1, 1],
         [1, 1, 0, 1],
         [0, 1, 1, 0]]
k = 2

print(partial_feedback_edge_set(graph, k))
