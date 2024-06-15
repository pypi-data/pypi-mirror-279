#Acyclic Partition

def acyclic_partition(graph):
    n = len(graph)
    dp = [float('inf')] * (1 << n)
    dp[0] = 0

    for mask in range(1 << n):
        for u in range(n):
            if mask & (1 << u) == 0:
                continue
            submask = mask ^ (1 << u)
            dp[mask] = min(dp[mask], dp[submask] + 1)

            for v in range(n):
                if (submask & (1 << v)) and graph[v][u] == 1:
                    dp[mask] = min(dp[mask], dp[submask])

    return dp[(1 << n) - 1]

# Example usage:
graph = [
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 0]
]
result = acyclic_partition(graph)
print("Minimum partitions:", result)
