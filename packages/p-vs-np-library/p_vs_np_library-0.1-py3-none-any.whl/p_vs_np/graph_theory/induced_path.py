##Induced Path

def dfs(graph, vertex, visited, path):
    visited.add(vertex)
    path.append(vertex)
    for neighbor in graph[vertex]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited, path)

def induced_path(graph):
    longest_path = []
    for vertex in graph:
        visited = set()
        path = []
        dfs(graph, vertex, visited, path)
        if len(path) > len(longest_path):
            longest_path = path
    return longest_path

graph = {
    0: {1, 2},
    1: {0, 2, 3},
    2: {0, 1, 3},
    3: {1, 2},
    4: {5, 6},
    5: {4, 6},
    6: {4, 5}
}

path = induced_path(graph)
print(path)
