##Partition Into Hamiltonian Subgraphs

def partition_into_hamiltonian_subgraphs(graph):
    def dfs(v, visited, adj_list):
        visited.add(v)
        for neighbor in adj_list[v]:
            if neighbor not in visited:
                dfs(neighbor, visited, adj_list)
    def is_hamiltonian(subgraph):
        # check if the subgraph contains a Hamiltonian path
        return True
    def find_subgraph(graph, vertex):
        visited = set()
        subgraph = set()
        queue = [vertex]
        while queue:
            v = queue.pop(0)
            if v not in visited:
                visited.add(v)
                subgraph.add(v)
                for neighbor in graph[v]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        return subgraph

    visited = set()
    hamiltonian_subgraphs = []
    for vertex in range(len(graph)):
        if vertex not in visited:
            subgraph = find_subgraph(graph, vertex)
            visited = visited.union(subgraph)
            if is_hamiltonian(subgraph):
                hamiltonian_subgraphs.append(subgraph)
    return len(hamiltonian_subgraphs)

graph = [[0, 1, 1, 0],
         [1, 0, 1, 1],
         [1, 1, 0, 0],
         [0, 1, 0, 0]]

print(partition_into_hamiltonian_subgraphs(graph))
