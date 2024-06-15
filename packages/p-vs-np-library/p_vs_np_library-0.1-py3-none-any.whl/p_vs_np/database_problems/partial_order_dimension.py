#Partial
Order
dimension

import itertools


def is_transitive(DAG, ordering):
    for u, v in itertools.combinations(ordering, 2):
        if (u, v) not in DAG.edges():
            return False
    return True


def partial_order_dimension(DAG, K):
    n = len(DAG.nodes())
    vertices = list(DAG.nodes())

    # Generate all possible combinations of K linear orderings
    orderings = list(itertools.permutations(vertices, K))

    # Check if each ordering satisfies the transitive property
    for ordering in orderings:
        if is_transitive(DAG, ordering):
            return True

    return False


# Example usage
if __name__ == '__main__':
    import networkx as nx

    # Example instance
    DAG = nx.DiGraph()
    DAG.add_edges_from([(1, 2), (2, 3), (1, 3)])
    K = 2

    # Solve the "Partial Order Dimension" problem
    result = partial_order_dimension(DAG, K)

    # Print the result
    if result:
        print("DAG has a collection of linear orderings satisfying the constraints")
    else:
        print("DAG does not have a collection of linear orderings satisfying the constraints")

