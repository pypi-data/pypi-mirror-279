#Safety of Database Transaction Systems(*)


def is_serializable(T, H):
    # Generate all possible permutations of the transactions
    permutations = get_permutations(T)

    # Check if any permutation results in an equivalent serial history
    for permutation in permutations:
        serial_history = execute_serially(permutation)
        if is_equivalent(H, serial_history):
            return True

    return False


def get_permutations(T):
    # Use itertools library to generate all permutations of T
    from itertools import permutations
    return permutations(T)


def execute_serially(transactions):
    # Execute transactions serially and return the resulting history
    history = []
    for transaction in transactions:
        # Execute the transaction and update the history
        history += execute_transaction(transaction)
    return history


def execute_transaction(transaction):
    # Execute a single transaction and return the list of operations
    # You would need to implement the logic specific to your transaction system
    # Here, I'm assuming a simple list-based representation of the history
    return transaction


def is_equivalent(history1, history2):
    # Compare the two histories and check if they are equivalent
    # You would need to implement the logic specific to your transaction system
    # Here, I'm assuming a simple list-based representation of the history
    return history1 == history2


# Example usage
transactions = ['T1', 'T2', 'T3']  # List of transactions T
history = ['A', 'B', 'C']  # Transaction history H

result = is_serializable(transactions, history)
print(result)
