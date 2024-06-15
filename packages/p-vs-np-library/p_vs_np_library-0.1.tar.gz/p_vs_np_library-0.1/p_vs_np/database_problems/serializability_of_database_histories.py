#Serializability of database histories

from collections import defaultdict


def is_serializable(transactions, precedence):
    graph = build_precedence_graph(precedence)
    visited = set()

    for transaction in transactions:
        if not dfs(graph, transaction, visited, set()):
            return False

    return True


def build_precedence_graph(precedence):
    graph = defaultdict(list)

    for (t1, t2) in precedence:
        graph[t1].append(t2)

    return graph


def dfs(graph, transaction, visited, path):
    if transaction in visited:
        return True

    if transaction in path:
        return False

    visited.add(transaction)
    path.add(transaction)

    for neighbor in graph[transaction]:
        if not dfs(graph, neighbor, visited, path):
            return False

    path.remove(transaction)
    return True


# Example usage
transactions = ['T1', 'T2', 'T3']
precedence = [('T1', 'T2'), ('T2', 'T3')]

result = is_serializable(transactions, precedence)
if result:
    print("The database history is serializable.")
else:
    print("The database history is not serializable.")
