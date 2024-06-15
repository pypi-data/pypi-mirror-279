#Graph Homomorphism

from networkx.algorithms.isomorphism import GraphMatcher

# Define the graphs
G = nx.Graph()
H = nx.Graph()

# Add edges and nodes to the graphs
G.add_edges_from([(1,2), (2,3), (3,4)])
H.add_edges_from([(5,6), (6,7), (7,8)])

# Create a GraphMatcher object
gm = GraphMatcher(G, H)

# Check for graph homomorphism
if gm.subgraph_is_isomorphic():
    print("There exists a homomorphism from G to H.")
else:
    print("There is no homomorphism from G to H.")
