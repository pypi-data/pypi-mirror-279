#Induced Subgraph With Property ∏

def induced_subgraph_with_property(graph, property_function):
    def is_subset(subset, set):
        for element in subset:
            if element not in set:
                return False
        return True

    def is_induced_subgraph(subgraph, set):
        for vertex in subgraph:
            for neighbor in graph[vertex]:
                if neighbor not in set and neighbor in subgraph:
                    return False
        return True

    def power_set(s):
        x = len(s)
        power_set = []
        for i in range(1 << x):
            subset = [s[j] for j in range(x) if (i & (1 << j))]
            power_set.append(subset)
        return power_set

    def find_induced_subgraph(graph, property_function):
        max_subgraph = []
        for subset in power_set(graph.keys()):
            if is_induced_subgraph(subset, graph.keys()) and property_function(subset):
                if len(subset) > len(max_subgraph):
                    max_subgraph = subset
        return max_subgraph

    return find_induced_subgraph(graph, property_function)

def is_clique(subgraph):
    for vertex in subgraph:
        for neighbor in subgraph:
            if vertex != neighbor and neighbor not in graph[vertex]:
                return False
    return True

graph = {
    0: {1, 2},
    1: {0, 2},
    2: {0, 1, 3},
    3: {2},
    4: {5, 6},
    5: {4, 6},
    6: {4, 5}
}

induced_subgraph = induced_subgraph_with_property(graph, is_clique)

print(induced_subgraph)
