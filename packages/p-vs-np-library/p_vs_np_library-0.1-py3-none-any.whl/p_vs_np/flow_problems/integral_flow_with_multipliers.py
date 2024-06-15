#Integral Flow With Multipliers

from pulp import *

def solve_integral_flow_with_multipliers(graph, multipliers):
    # Create a minimization problem
    prob = LpProblem("Integral Flow", LpMinimize)

    # Decision variables
    flow_vars = LpVariable.dicts("Flow", graph.edges(), lowBound=0, cat="Integer")

    # Objective function
    prob += lpSum(flow_vars[edge] * graph[edge[0]][edge[1]]['cost'] * multipliers[edge]
                  for edge in graph.edges())

    # Constraints
    for node in graph.nodes():
        inflow = lpSum(flow_vars[(i, node)] for i in graph.predecessors(node))
        outflow = lpSum(flow_vars[(node, j)] for j in graph.successors(node))
        prob += inflow - outflow == 0

    # Capacity constraints
    for edge in graph.edges():
        prob += flow_vars[edge] <= graph[edge[0]][edge[1]]['capacity']

    # Solve the problem
    prob.solve()

    # Retrieve the solution
    flow_dict = {(edge[0], edge[1]): int(flow_vars[edge].varValue) for edge in graph.edges()}

    # Return the objective value and flow dictionary
    return value(prob.objective), flow_dict

# Example usage:
graph = nx.DiGraph()

# Add edges with capacities, costs, and multipliers
graph.add_edge('A', 'B', capacity=5, cost=2)
graph.add_edge('A', 'C', capacity=3, cost=3)
graph.add_edge('B', 'C', capacity=2, cost=1)
graph.add_edge('B', 'D', capacity=4, cost=4)
graph.add_edge('C', 'D', capacity=3, cost=2)

# Set the multipliers for edges
multipliers = {('A', 'B'): 1, ('A', 'C'): 2, ('B', 'C'): 3, ('B', 'D'): 1, ('C', 'D'): 2}

objective_value, flow_dict = solve_integral_flow_with_multipliers(graph, multipliers)

print("Objective Value:", objective_value)
print("Flow on Edges:")
for edge, flow in flow_dict.items():
    print(f"{edge[0]} -> {edge[1]}: {flow}")
