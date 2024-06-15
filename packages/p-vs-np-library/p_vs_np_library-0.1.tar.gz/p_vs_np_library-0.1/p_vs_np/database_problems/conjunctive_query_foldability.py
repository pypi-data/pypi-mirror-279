#Conjunctive Query Foldability

def is_conjunctive_query_foldable(R, Q):
    # Generate all possible subsets of relations
    subsets = generate_subsets(R)

    for subset in subsets:
        result = evaluate_query(subset, Q)
        if result == Q:
            return True

    return False

def generate_subsets(R):
    subsets = [[]]

    for r in R:
        new_subsets = []
        for subset in subsets:
            new_subsets.append(subset + [r])
        subsets.extend(new_subsets)

    return subsets

def evaluate_query(relations, Q):
    result = []

    for q in Q:
        if isinstance(q, tuple):  # Atomic formula
            relation = q[0]
            attribute = q[1]
            if relation in relations:
                result.append(q)
        else:  # Connective
            operator = q[0]
            operands = q[1:]
            evaluated_operands = [evaluate_query(relations, op) for op in operands]
            result.append((operator, *evaluated_operands))

    return tuple(result)

# Example usage
R = ['R1', 'R2', 'R3']
Q = [('R1', 'A'), ('R2', 'B'), ('R3', 'C')]

result = is_conjunctive_query_foldable(R, Q)
if result:
    print("Conjunctive query is foldable.")
else:
    print("Conjunctive query is not foldable.")

