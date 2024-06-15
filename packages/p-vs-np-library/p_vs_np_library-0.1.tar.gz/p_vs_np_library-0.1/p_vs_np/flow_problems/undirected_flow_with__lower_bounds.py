#Undirected Flow With  Lower Bounds

from pulp import *

def solve_undirected_flow_with_lower_bounds(graph, lower_bounds):
    # Create a minimization problem
    prob = LpProblem("Undirected Flow", LpMinimize)

    # Decision variables
    flow_vars = LpVariable.dicts("Flow", graph.edges(), lowBound=0)

    # Objective function
    prob += lpSum(flow_vars[edge] for edge in graph.edges())

    # Constraints
    for node in graph.nodes():
        inflow = lpSum(flow_vars[(i, node)] for i in graph.neighbors(node))
        outflow = lpSum(flow_vars[(node, j)] for j in graph.neighbors(node))
        prob += inflow - outflow == 0

    # Lower bound constraints
    for edge in graph.edges():
        prob += flow_vars[edge] >= lower_bounds[edge]

    # Solve the problem
    prob.solve()

    # Retrieve the solution
    flow_dict = {(edge[0], edge[1]): flow_vars[edge].varValue for edge in graph.edges()}

    # Return the objective value and flow dictionary
    return value(prob.objective), flow_dict

# Example usage:
graph = nx.Graph()

# Add edges with lower bounds
graph.add_edge('A', 'B', lower_bound=2)
graph.add_edge('A', 'C', lower_bound=3)
graph.add_edge('B', 'C', lower_bound=1)
graph.add_edge('B', 'D', lower_bound=0)
graph.add_edge('C', 'D', lower_bound=2)

# Set the lower bounds for edges
lower_bounds = {('A', 'B'): 2, ('A', 'C'): 3, ('B', 'C'): 1, ('B', 'D'): 0, ('C', 'D'): 2}

objective_value, flow_dict = solve_undirected_flow_with_lower_bounds(graph, lower_bounds)

print("Objective Value:", objective_value)
print("Flow on Edges:")
for edge, flow in flow_dict.items():
    print(f"{edge[0]} - {edge[1]}: {flow}")
