#Hamiltonian Completion

from itertools import permutations

def hamiltonian_completion(graph, edges):
    for cycle in permutations(edges):
        if len(cycle) == graph.number_of_nodes():
            if cycle[0] in graph.successors(cycle[-1]):
                return list(cycle) + [cycle[0]]
    return None

graph = nx.Graph()
graph.add_edges_from([(0, 1), (1, 2), (2, 3)])

edges = [(0, 1), (1, 2)]

cycle = hamiltonian_completion(graph, edges)

print(cycle)
