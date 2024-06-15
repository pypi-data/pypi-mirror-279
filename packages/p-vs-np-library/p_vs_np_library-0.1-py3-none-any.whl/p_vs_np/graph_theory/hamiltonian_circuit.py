#Hamiltonian Circuit

def is_safe(v, pos, path):
    if graph[path[pos-1]][v] == 0:
        return False
    for vertex in path:
        if vertex == v:
            return False
    return True

def hamiltonian_cycle_util(path, pos):
    if pos == V:
        if graph[path[pos-1]][path[0]] == 1:
            return True
        else:
            return False
    for v in range(1, V):
        if is_safe(v, pos, path) == True:
            path[pos] = v
            if hamiltonian_cycle_util(path, pos+1) == True:
                return True
            path[pos] = -1
    return False

def hamiltonian_cycle(graph):
    path = [-1] * V
    path[0] = 0
    if hamiltonian_cycle_util(path, 1) == False:
        print("Solution does not exist")
    else:
        print(path)

V = 5
graph = [[0, 1, 0, 1, 0],
         [1, 0, 1, 1, 1],
         [0, 1, 0, 0, 1],
         [1, 1, 0, 0, 1],
         [0, 1, 1, 1, 0]]
hamiltonian_cycle(graph)
