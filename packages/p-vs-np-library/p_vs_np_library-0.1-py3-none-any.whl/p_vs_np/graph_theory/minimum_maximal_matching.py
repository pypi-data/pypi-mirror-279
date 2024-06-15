#Minimum Maximal Matching


def minimum_maximal_matching(graph):
    def dfs(v, visited, adj_list, match):
        visited.add(v)
        for neighbor in adj_list[v]:
            if neighbor not in visited:
                if match[neighbor] == -1 or dfs(match[neighbor], visited, adj_list, match):
                    match[v] = neighbor
                    match[neighbor] = v
                    return True
        return False

    match = [-1] * len(graph)
    matching = 0
    for i in range(len(graph)):
        if match[i] == -1:
            visited = set()
            if dfs(i, visited, graph, match):
                matching += 1
    return matching


graph = [[0, 1, 1, 0],
         [1, 0, 1, 1],
         [1, 1, 0, 0],
         [0, 1, 0, 0]]

print(minimum_maximal_matching(graph))
