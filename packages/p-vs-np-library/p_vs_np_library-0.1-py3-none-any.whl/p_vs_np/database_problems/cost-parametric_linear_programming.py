#Cost-Parametric Linear Programming

import cvxpy as cp
import numpy as np


def solve_cost_parametric_linear_programming(cost_parameter):
    # Define the variables
    x = cp.Variable(2)

    # Define the objective function
    c = cp.Parameter(2)  # Parameterized cost coefficients
    objective = cp.Minimize(c.T @ x)

    # Define the constraints
    constraints = [x >= 0, x[0] + x[1] <= 1]

    # Create the problem
    problem = cp.Problem(objective, constraints)

    # Set the cost parameter value
    c.value = cost_parameter

    # Solve the problem
    problem.solve()

    # Print the solution
    if problem.status == "optimal":
        print("Optimal solution found for cost parameter =", cost_parameter)
        print("x =", x.value)
        print("Objective =", problem.value)
    else:
        print("No feasible solution found for cost parameter =", cost_parameter)


# Example usage
if __name__ == "__main__":
    cost_parameter = 1.0  # Example cost parameter
    solve_cost_parametric_linear_programming(cost_parameter)
