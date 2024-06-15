#Expected Retrieval Costs

import itertools

def calculate_cost(partitions, p, K):
    total_cost = 0

    for i, Ri in enumerate(partitions):
        for j, Rj in enumerate(partitions):
            cost = calculate_pair_cost(Ri, Rj, i, j)
            total_cost += p[i] * p[j] * cost

            if total_cost > K:
                return False

    return True

def calculate_pair_cost(Ri, Rj, i, j):
    m = len(Ri)

    if 1 <= i < j <= m:
        return j - i - 1
    elif 1 <= j < i <= m:
        return m - i + j - 1

def find_partition(R, p, K):
    n = len(R)
    partitions = list(itertools.chain.from_iterable(itertools.combinations(R, r) for r in range(1, n + 1)))

    for partition in partitions:
        if calculate_cost(partition, p, K):
            return partition

    return None

# Example usage
R = [1, 2, 3, 4]
p = [1, 2, 3, 4]
K = 50

result = find_partition(R, p, K)
if result:
    print("A valid partition exists:")
    for subset in result:
        print(subset)
else:
    print("No valid partition found.")
