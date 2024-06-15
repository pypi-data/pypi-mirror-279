#Subgraph Isomorphism

from networkx.algorithms.isomorphism import GraphMatcher

# Define the graphs to be compared
G1 = nx.Graph()
G2 = nx.Graph()

# Add edges and nodes to the graphs
G1.add_edges_from([(1,2), (2,3), (3,4)])
G2.add_edges_from([(5,6), (6,7), (7,8)])

# Create a GraphMatcher object
gm = GraphMatcher(G1, G2)

# Check for subgraph isomorphism
if gm.subgraph_is_isomorphic():
    print("The graphs are subgraph isomorphic.")
else:
    print("The graphs are not subgraph isomorphic.")
