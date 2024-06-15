#Directed Hamiltonian Circuit

def is_safe(v, graph, path, pos):
    if graph[path[pos-1]][v] == 0:
        return False
    for vertex in path:
        if vertex == v:
            return False
    return True

def hamiltonian_path_util(graph, path, pos):
    if pos == V:
        if graph[path[pos-1]][path[0]] == 1:
            return True
        else:
            return False
    for v in range(V):
        if is_safe(v, graph, path, pos):
            path[pos] = v
            if hamiltonian_path_util(graph, path, pos+1) == True:
                return True
            path[pos] = -1
    return False

def hamiltonian_path(graph):
    path = [-1] * V
    path[0] = 0
    if hamiltonian_path_util(graph, path, 1) == False:
        print("Solution does not exist")
    else:
        print(path)

V = 5
graph = [[0, 1, 0, 1, 0],
         [0, 0, 1, 0, 1],
         [0, 0, 0, 1, 0],
         [0, 0, 0, 0, 1],
         [0, 0, 0, 0, 0]]
hamiltonian_path(graph)
