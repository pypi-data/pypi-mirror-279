#ETOL Grammar Non-Emptiness

def is_etol_grammar_non_empty(grammar):
    # Create a set to keep track of visited non-terminals
    visited = set()

    # Perform depth-first search starting from the start symbol
    dfs(grammar, grammar['start_symbol'], visited)

    # Check if any non-terminal was visited, indicating non-emptiness
    return bool(visited)


def dfs(grammar, symbol, visited):
    # Base case: symbol is a terminal, stop recursion
    if symbol not in grammar:
        return

    # Mark the symbol as visited
    visited.add(symbol)

    # Recursively visit the production rules
    for production in grammar[symbol]:
        for token in production:
            dfs(grammar, token, visited)


# Example usage
grammar = {
    'start_symbol': 'S',
    'S': ['aA', 'bB'],
    'A': ['aA', ''],
    'B': ['bB', '']
}

etol_non_empty = is_etol_grammar_non_empty(grammar)
print(f"ETOL Grammar Non-Emptiness: {etol_non_empty}")
