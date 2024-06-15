#Fault Detection in Directed Graphs

from itertools import combinations

def fault_detection_in_directed_graphs(G, I, O, K):
    # Check if K > |I| * |O|
    if K > len(I) * len(O):
        return True

    # Generate all possible test sets of size K or less
    test_sets = []
    for k in range(K + 1):
        test_sets.extend(combinations(I, k))

    # Check if any test set can detect every single fault
    for test_set in test_sets:
        if is_fault_detected(G, test_set):
            return True

    return False

def is_fault_detected(G, test_set):
    for v in G:
        for u1, u2 in test_set:
            if is_reachable(G, u1, u2, v):
                break
        else:
            return False

    return True

def is_reachable(G, u1, u2, v):
    stack = [u1]
    visited = set()

    while stack:
        current = stack.pop()

        if current == u2:
            return True

        visited.add(current)

        for neighbor in G[current]:
            if neighbor not in visited:
                stack.append(neighbor)

    return False

# Example usage
if __name__ == '__main__':
    # Example instance
    G = {
        'v1': ['v2'],
        'v2': ['v3', 'v4'],
        'v3': ['v4'],
        'v4': []
    }

    I = ['v1']
    O = ['v4']
    K = 3

    # Solve the "FAULT DETECTION IN DIRECTED GRAPHS" problem
    result = fault_detection_in_directed_graphs(G, I, O, K)

    # Print the result
    if result:
        print("Fault detected!")
    else:
        print("No fault detected!")
