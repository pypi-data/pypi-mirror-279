#Degree-Bounded Connected Subgraph

def degree_bounded_connected_subgraph(graph, degree_bound):
    def dfs(graph, vertex, visited, subgraph):
        visited.add(vertex)
        subgraph.append(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                dfs(graph, neighbor, visited, subgraph)

    def is_degree_bounded(subgraph, graph, degree_bound):
        for vertex in subgraph:
            if len(graph[vertex]) > degree_bound:
                return False
        return True

    max_subgraph = []
    for vertex in graph:
        visited = set()
        subgraph = []
        dfs(graph, vertex, visited, subgraph)
        if len(subgraph) > len(max_subgraph) and is_degree_bounded(subgraph, graph, degree_bound):
            max_subgraph = subgraph
    return max_subgraph

graph = {
    0: {1, 2},
    1: {0, 2, 3},
    2: {0, 1, 3},
    3: {1, 2, 4, 5},
    4: {3, 5},
    5: {3, 4}
}

degree_bound = 2

subgraph = degree_bounded_connected_subgraph(graph, degree_bound)

print(subgraph)
