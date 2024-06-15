#Feasible Basis Extension

from scipy.optimize import linprog

def solve_feasible_basis_extension(c, A_eq, b_eq, A_ub, b_ub):
    # Solve the linear programming problem
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq)

    # Check if the problem is feasible
    if result.success:
        print("Feasible basis extension found.")
        print("Optimal solution:", result.x)
    else:
        print("No feasible basis extension found.")

# Example usage
if __name__ == "__main__":
    # Define the linear programming problem
    c = [-1, -1]  # Objective function coefficients
    A_eq = [[2, 1]]  # Equality constraint matrix
    b_eq = [3]  # Equality constraint vector
    A_ub = [[-1, 1]]  # Inequality constraint matrix
    b_ub = [1]  # Inequality constraint vector

    # Solve the "Feasible Basis Extension" problem
    solve_feasible_basis_extension(c, A_eq, b_eq, A_ub, b_ub)

