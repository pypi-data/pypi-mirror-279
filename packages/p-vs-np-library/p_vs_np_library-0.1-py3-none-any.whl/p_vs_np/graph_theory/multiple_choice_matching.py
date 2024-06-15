#Multiple Choice Matching

from scipy.optimize import linprog

# Define the weight matrix
weights = [[2, 4, 1], [3, 2, 4], [1, 3, 2], [4, 1, 3]]

# Define the number of items and agents
num_items = len(weights)
num_agents = len(weights[0])

# Define the constraints
c = [1 for i in range(num_items*num_agents)]
A_eq = [[[1 if i == j else 0 for i in range(num_items) for j in range(num_agents)], [1 for i in range(num_items)]] for j in range(num_agents)]
b_eq = [1 for i in range(num_agents)]

# Define the bounds
bnds = [(0, 1) for i in range(num_items*num_agents)]

# Solve the linear program
res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bnds, method='simplex')

# Print the result
print("Optimal value:", res.fun)
print("Optimal solution:", res.x)
