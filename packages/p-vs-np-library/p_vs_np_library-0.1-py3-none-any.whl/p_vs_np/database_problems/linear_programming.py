#Linear Programming

from pulp import LpProblem, LpVariable, LpMinimize, lpSum, value

def linear_programming(V, D, C, B):
    # Create a linear programming problem
    prob = LpProblem("LinearProgramming", LpMinimize)

    # Create variables
    X = [LpVariable(f"X{i}", lowBound=0) for i in range(len(V))]

    # Set objective function
    prob += lpSum(C[i] * X[i] for i in range(len(V)))

    # Add constraints
    for j in range(len(D)):
        prob += lpSum(V[j][i] * X[i] for i in range(len(V))) <= D[j]

    # Add additional constraint
    prob += lpSum(C[i] * X[i] for i in range(len(V))) - B >= 0

    # Solve the problem
    prob.solve()

    # Check if a feasible solution exists
    if prob.status == 1:
        return True, [value(X[i]) for i in range(len(V))]
    else:
        return False, []

# Example usage
if __name__ == '__main__':
    # Example instance
    V = [[1, 2, 3], [4, 5, 6]]
    D = [10, 20]
    C = [1, 1, 1]
    B = 15

    # Solve the "Linear Programming" problem
    feasible, solution = linear_programming(V, D, C, B)

    # Print the result
    if feasible:
        print("A feasible solution exists:")
        print(solution)
    else:
        print("No feasible solution exists.")
