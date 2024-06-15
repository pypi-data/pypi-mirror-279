#Digraph D-Morphism

from networkx.algorithms.isomorphism import DiGraphMatcher

# Define the directed graphs
G = nx.DiGraph()
H = nx.DiGraph()

# Add edges and nodes to the graphs
G.add_edges_from([(1,2), (2,3), (3,4)])
H.add_edges_from([(5,6), (6,7), (7,8)])

# Create a DiGraphMatcher object
gm = DiGraphMatcher(G, H)

# Check for digraph d-morphism
if gm.subgraph_is_isomorphic():
    print("There exists a d-morphism from G to H.")
else:
    print("There is no d-morphism from G to H.")
