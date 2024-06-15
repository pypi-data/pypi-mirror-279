#Minimizing Dummy Activities in PERT Networks

def minimize_dummy_activities_pert_network(adjacency_matrix):
    n = len(adjacency_matrix)  # Number of nodes in the PERT network

    # Calculate the indegree of each node
    indegree = [sum(adjacency_matrix[j][i] for j in range(n)) for i in range(n)]

    # Initialize the dynamic programming table
    dp = [[float('inf')] * n for _ in range(n)]
    dp[0][0] = 0

    # Iterate through the PERT network
    for i in range(n):
        for j in range(n):
            if dp[i][j] == float('inf'):
                continue

            for k in range(n):
                if adjacency_matrix[j][k] != 0:
                    dp[i + 1][k] = min(dp[i + 1][k], dp[i][j] + (indegree[k] - 1))

    # Find the minimum number of dummy activities
    min_dummy_activities = min(dp[-1])

    return min_dummy_activities

# Example usage:
adjacency_matrix = [
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 0]
]

min_dummy_activities = minimize_dummy_activities_pert_network(adjacency_matrix)

print("Minimum number of dummy activities:", min_dummy_activities)
