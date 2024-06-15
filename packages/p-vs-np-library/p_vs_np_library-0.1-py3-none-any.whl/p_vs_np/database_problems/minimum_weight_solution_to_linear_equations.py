#Minimum Weight Solution to Linear Equations

import numpy as np

def solve_minimum_weight_solution(A, b):
    # Solve the linear system of equations
    x = np.linalg.lstsq(A, b, rcond=None)[0]

    # Print the minimum weight solution
    print("Minimum weight solution:", x)

# Example usage
if __name__ == "__main__":
    # Define the coefficients matrix and the constant vector
    A = np.array([[2, 1], [1, 3], [1, 1]])  # Coefficients matrix
    b = np.array([4, 5, 3])  # Constant vector

    # Solve the "Minimum Weight Solution to Linear Equations" problem
    solve_minimum_weight_solution(A, b)

