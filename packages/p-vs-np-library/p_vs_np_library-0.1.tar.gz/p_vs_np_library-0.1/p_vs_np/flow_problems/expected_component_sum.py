#Expected Component Sum

def expected_component_sum(graph, values):
    n = len(graph)
    memo = [[-1] * (1 << n) for _ in range(n)]

    return calculate_expected_sum(graph, values, 0, 1, memo)

def calculate_expected_sum(graph, values, node, subset, memo):
    if subset == (1 << len(graph)) - 1:
        return values[node]

    if memo[node][subset] != -1:
        return memo[node][subset]

    expected_sum = 0

    for neighbor in graph[node]:
        if subset & (1 << neighbor) == 0:
            expected_sum += calculate_expected_sum(graph, values, neighbor, subset | (1 << neighbor), memo)

    memo[node][subset] = values[node] + expected_sum
    return memo[node][subset]

# Example usage:
graph = [[1, 2], [0], [0]]
values = [3, 4, 5]

expected_sum = expected_component_sum(graph, values)

print("Expected Component Sum:", expected_sum)
