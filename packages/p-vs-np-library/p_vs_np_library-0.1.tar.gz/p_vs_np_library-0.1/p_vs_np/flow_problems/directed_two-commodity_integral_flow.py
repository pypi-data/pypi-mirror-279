#Directed Two-Commodity Integral Flow

from pulp import *

def solve_directed_two_commodity_integral_flow(graph, demands, capacities):
    # Create a maximization problem
    prob = LpProblem("Directed Two-Commodity Flow", LpMaximize)

    # Decision variables
    flow_vars = LpVariable.dicts("Flow", graph.edges(), lowBound=0, cat="Integer")

    # Objective function
    prob += lpSum(flow_vars[edge] for edge in graph.edges())

    # Constraints
    for node in graph.nodes():
        inflow = lpSum(flow_vars[(i, node)] for i in graph.predecessors(node))
        outflow = lpSum(flow_vars[(node, j)] for j in graph.successors(node))
        prob += inflow - outflow == demands[node]

    # Capacity constraints
    for edge in graph.edges():
        prob += flow_vars[edge] <= capacities[edge]

    # Solve the problem
    prob.solve()

    # Retrieve the solution
    flow_dict = {(edge[0], edge[1]): int(flow_vars[edge].varValue) for edge in graph.edges()}

    # Return the objective value and flow dictionary
    return value(prob.objective), flow_dict

# Example usage:
graph = nx.DiGraph()

# Add edges with capacities
graph.add_edge('A', 'B', capacity=5)
graph.add_edge('A', 'C', capacity=3)
graph.add_edge('B', 'C', capacity=2)
graph.add_edge('B', 'D', capacity=4)
graph.add_edge('C', 'D', capacity=3)

# Set the demands for nodes
demands = {'A': -5, 'D': 5}

# Set the capacities for edges
capacities = {('A', 'B'): 5, ('A', 'C'): 3, ('B', 'C'): 2, ('B', 'D'): 4, ('C', 'D'): 3}

objective_value, flow_dict = solve_directed_two_commodity_integral_flow(graph, demands, capacities)

print("Objective Value:", objective_value)
print("Flow on Edges:")
for edge, flow in flow_dict.items():
    print(f"{edge[0]} -> {edge[1]}: {flow}")
