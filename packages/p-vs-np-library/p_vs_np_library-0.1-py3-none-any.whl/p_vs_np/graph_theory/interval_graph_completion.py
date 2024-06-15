#Interval Graph Completion

from itertools import combinations

def interval_graph_completion(graph):
    for edges in combinations(graph.edges(), graph.number_of_edges()):
        subgraph = graph.subgraph(edges)
        if nx.is_chordal(subgraph):
            return subgraph
    return None

graph = nx.Graph()
graph.add_edges_from([(0, 1), (1, 2)])

subgraph = interval_graph_completion(graph)

print(subgraph.edges())
