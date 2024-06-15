#Open Hemisphere

from pulp import LpProblem, LpVariable, LpMaximize

def solve_open_hemisphere(X, K):
    # Create the linear programming problem
    prob = LpProblem("Open Hemisphere Problem", LpMaximize)

    # Define the decision variables
    y = [LpVariable(f"y{i}", lowBound=0, cat="Continuous") for i in range(len(X[0]))]

    # Define the objective function
    prob += sum(y)

    # Define the constraints
    for x in X:
        prob += sum(xi * yi for xi, yi in zip(x, y)) >= 1

    # Add the additional constraint for at least K solutions
    prob += sum(1 for x in X for xi in x for yi in y if xi * yi > 0) >= K

    # Solve the problem
    prob.solve()

    if prob.status == 1:
        # Problem is feasible, return the optimal solution
        solution = [v.varValue for v in y]
        return solution
    else:
        # Problem is infeasible
        return None

# Example usage
X = [[1, 2, 3], [-1, -2, 1], [0, 1, -1]]
K = 2

solution = solve_open_hemisphere(X, K)
if solution:
    print("Feasible solution:", solution)
else:
    print("No feasible solution found.")
