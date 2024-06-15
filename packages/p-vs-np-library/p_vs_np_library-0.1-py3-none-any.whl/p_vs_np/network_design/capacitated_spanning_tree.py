#Capacitated Spanning Tree

from pulp import *

def capacitated_spanning_tree(n, edges, capacity):
    # Create the LP problem
    prob = LpProblem("Capacitated Spanning Tree", LpMinimize)

    # Create the binary decision variables
    x = {(u, v): LpVariable(f"x_{u}_{v}", 0, 1, LpBinary) for u, v, w in edges}

    # Create the objective function
    prob += lpSum([x[u, v] * w for u, v, w in edges]), "Total Edge Weight"

    # Add the degree constraints
    for i in range(n):
        prob += lpSum([x[u, v] for u, v in x.keys() if u == i]) == 2, f"Degree of {i}"

    # Add the capacity constraints
    for u, v, w in edges:
        prob += x[u,v] * w <= capacity

    # Solve the LP problem
    prob.solve()

    # Extract the solution
    tree = [(u, v) for u, v in x.keys() if x[u, v].value() == 1.0]
    return tree
