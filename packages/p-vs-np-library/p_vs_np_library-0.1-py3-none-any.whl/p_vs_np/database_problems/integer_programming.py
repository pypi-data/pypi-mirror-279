#Integer Programming

from pulp import LpProblem, LpVariable, LpInteger, LpMaximize, LpStatus, lpSum


def solve_integer_programming():
    # Create the LP problem
    problem = LpProblem("Integer Programming", LpMaximize)

    # Decision variables
    x = LpVariable("x", lowBound=0, cat=LpInteger)
    y = LpVariable("y", lowBound=0, cat=LpInteger)

    # Objective function
    problem += 3 * x + 2 * y

    # Constraints
    problem += 2 * x + y <= 8
    problem += x + 2 * y <= 9

    # Solve the problem
    problem.solve()

    # Print the solution
    if problem.status == LpStatusOptimal:
        print("Optimal solution found:")
        print("x =", x.varValue)
        print("y =", y.varValue)
        print("Objective =", problem.objective.value())
    else:
        print("No feasible solution found.")


# Example usage
if __name__ == "__main__":
    solve_integer_programming()

