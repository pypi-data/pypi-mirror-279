#Minimum Edge-Cost Flow

import networkx as nx

def solve_minimum_cost_flow(graph):
    flow_cost, flow_dict = nx.network_simplex(graph)
    return flow_cost, flow_dict

# Example usage:
graph = nx.DiGraph()

# Add edges with capacities and costs
graph.add_edge('A', 'B', capacity=5, weight=2)
graph.add_edge('A', 'C', capacity=3, weight=3)
graph.add_edge('B', 'C', capacity=2, weight=1)
graph.add_edge('B', 'D', capacity=4, weight=4)
graph.add_edge('C', 'D', capacity=3, weight=2)

# Set the supply/demand for nodes
graph.nodes['A']['demand'] = -5
graph.nodes['D']['demand'] = 5

flow_cost, flow_dict = solve_minimum_cost_flow(graph)

print("Minimum Cost Flow:", flow_cost)
print("Flow on Edges:")
for u, v, flow in flow_dict.edges(data='flow'):
    print(f"{u} -> {v}: {flow}")
