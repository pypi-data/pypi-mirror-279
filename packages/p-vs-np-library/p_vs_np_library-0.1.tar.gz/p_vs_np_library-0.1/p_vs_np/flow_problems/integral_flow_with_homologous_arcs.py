#Integral Flow With Homologous Arcs

from pulp import *

def solve_integral_flow_with_homologous_arcs(graph, demands, homology_constraints):
    # Create a minimization problem
    prob = LpProblem("Integral Flow", LpMinimize)

    # Decision variables
    flow_vars = LpVariable.dicts("Flow", graph.edges(), lowBound=0, cat="Integer")

    # Objective function
    prob += lpSum(flow_vars[edge] * graph[edge[0]][edge[1]]['cost'] for edge in graph.edges())

    # Constraints
    for node in graph.nodes():
        inflow = lpSum(flow_vars[(i, node)] for i in graph.predecessors(node))
        outflow = lpSum(flow_vars[(node, j)] for j in graph.successors(node))
        prob += inflow - outflow == demands[node]

    # Homology constraints
    for constraint in homology_constraints:
        prob += lpSum(flow_vars[edge] for edge in constraint) == 0

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

# Add edges with capacities and costs
graph.add_edge('A', 'B', capacity=5, cost=2)
graph.add_edge('A', 'C', capacity=3, cost=3)
graph.add_edge('B', 'C', capacity=2, cost=1)
graph.add_edge('B', 'D', capacity=4, cost=4)
graph.add_edge('C', 'D', capacity=3, cost=2)

# Set the demands for nodes
demands = {'A': -5, 'D': 5}

# Set the homology constraints
homology_constraints = [[('A', 'B'), ('B', 'C'), ('C', 'D')],
                        [('A', 'C'), ('C', 'D')],
                        [('A', 'B'), ('B', 'D')]]

objective_value, flow_dict = solve_integral_flow_with_homologous_arcs(graph, demands, homology_constraints)

print("Objective Value:", objective_value)
print("Flow on Edges:")
for edge, flow in flow_dict.items():
    print(f"{edge[0]} -> {edge[1]}: {flow}")

