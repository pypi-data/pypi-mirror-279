#Quadratic Programming

import cvxpy as cp
import numpy as np


def solve_quadratic_programming():
    # Define the variables
    x = cp.Variable(2)

    # Define the objective function
    Q = np.array([[2, -1], [-1, 4]])
    c = np.array([1, -2])
    objective = cp.Minimize(cp.quad_form(x, Q) + c.T @ x)

    # Define the constraints
    constraints = [x >= 0, x[0] + x[1] <= 1]

    # Create the problem
    problem = cp.Problem(objective, constraints)

    # Solve the problem
    problem.solve()

    # Print the solution
    if problem.status == "optimal":
        print("Optimal solution found:")
        print("x =", x.value)
        print("Objective =", problem.value)
    else:
        print("No feasible solution found.")


# Example usage
if __name__ == "__main__":
    solve_quadratic_programming()
