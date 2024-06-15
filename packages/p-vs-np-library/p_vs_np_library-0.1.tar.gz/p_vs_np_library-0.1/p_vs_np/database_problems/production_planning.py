#Production Planning

from pulp import LpProblem, LpVariable, LpMaximize, LpStatus, lpSum


def production_planning(products, resources, demands, capacities, costs, profits):
    # Create the LP problem
    problem = LpProblem("Production Planning", LpMaximize)

    # Decision variables
    production = LpVariable.dicts("Production", products, lowBound=0, cat="Integer")

    # Objective function: maximize profit
    problem += lpSum(profits[i] * production[i] for i in products)

    # Constraints
    for r in resources:
        problem += lpSum(costs[i][r] * production[i] for i in products) <= capacities[r]

    for d in demands:
        problem += lpSum(production[i] for i in products if i in demands[d]) >= demands[d]

    # Solve the problem
    problem.solve()

    # Print the solution
    if problem.status == LpStatusOptimal:
        print("Production quantities:")
        for i in products:
            print(f"{i}: {production[i].varValue}")
        print("Total Profit: ", lpSum(profits[i] * production[i].varValue for i in products))
    else:
        print("No feasible solution found.")


# Example usage
if __name__ == "__main__":
    # List of products
    products = ["Product1", "Product2", "Product3"]

    # List of resources
    resources = ["Resource1", "Resource2"]

    # Demands for each product
    demands = {
        "Demand1": ["Product1", "Product2"],
        "Demand2": ["Product1", "Product3"],
    }

    # Production capacities for each resource
    capacities = {
        "Resource1": 100,
        "Resource2": 200,
    }

    # Production costs for each product and resource
    costs = {
        "Product1": {"Resource1": 10, "Resource2": 20},
        "Product2": {"Resource1": 15, "Resource2": 25},
        "Product3": {"Resource1": 20, "Resource2": 30},
    }

    # Profits for each product
    profits = {
        "Product1": 50,
        "Product2": 60,
        "Product3": 70,
    }

    # Solve the production planning problem
    production_planning(products, resources, demands, capacities, costs, profits)

