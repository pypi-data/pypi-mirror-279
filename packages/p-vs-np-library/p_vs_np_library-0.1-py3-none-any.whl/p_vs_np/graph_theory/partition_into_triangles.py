#Partition into Triangles


def partition_into_triangles(graph):
    def dfs(v, visited, adj_list):
        visited.add(v)
        for neighbor in adj_list[v]:
            if neighbor not in visited:
                dfs(neighbor, visited, adj_list)

    def connected_components(graph):
        visited = set()
        components = []
        for vertex in range(len(graph)):
            if vertex not in visited:
                component = set()
                dfs(vertex, visited, graph)
                components.append(component)
        return components

    def triangles(graph):
        triangles_count = 0
        for vertex in range(len(graph)):
            for neighbor in range(vertex + 1, len(graph)):
                if graph[vertex][neighbor]:
                    for neighbor2 in range(neighbor + 1, len(graph)):
                        if graph[vertex][neighbor2] and graph[neighbor][neighbor2]:
                            triangles_count += 1
        return triangles_count

    components = connected_components(graph)
    triangles_count = 0
    for component in components:
        triangles_count += triangles(component)
    return triangles_count


graph = [[0, 1, 1, 0],
         [1, 0, 1, 1],
         [1, 1, 0, 0],
         [0, 1, 0, 0]]

print(partition_into_triangles(graph))
