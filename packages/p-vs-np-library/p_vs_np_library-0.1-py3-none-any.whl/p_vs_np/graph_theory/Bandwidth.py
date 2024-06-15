#Bandwidth

def bandwidth(graph,n):
    degree = [0 for i in range(n)]
    for i in range(n):
        for j in range(n):
            if graph[i][j]:
                degree[i] += 1
    q = []
    for i in range(n):
        if degree[i] == 1:
            q.append(i)
    while q:
        u = q.pop(0)
        for v in range(n):
            if graph[u][v]:
                degree[v] -= 1
                if degree[v] == 1:
                    q.append(v)
    return degree

graph = [[0, 1, 1, 1],
         [1, 0, 1, 0],
         [1, 1, 0, 1],
         [1, 0, 1, 0]]

n = 4
print(bandwidth(graph,n))
