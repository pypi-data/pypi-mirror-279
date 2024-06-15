#Reynolds Covering For Context-Free Grammars

from collections import defaultdict


def find_reynolds_cover(grammar):
    # Initialize an empty set of non-terminals
    non_terminals = set(grammar.keys())

    # Compute the set of terminals
    terminals = set()
    for productions in grammar.values():
        for production in productions:
            for symbol in production:
                if symbol.islower():
                    terminals.add(symbol)

    # Create a mapping of terminals to non-terminals that can generate them
    terminal_coverage = defaultdict(set)
    for non_terminal, productions in grammar.items():
        for production in productions:
            for symbol in production:
                if symbol in terminals:
                    terminal_coverage[symbol].add(non_terminal)

    # Find the minimum set of non-terminals that cover all terminals
    while terminals:
        max_coverage = set()
        max_terminal = None

        # Find the terminal with maximum coverage
        for terminal, cover in terminal_coverage.items():
            if len(cover) > len(max_coverage):
                max_coverage = cover
                max_terminal = terminal

        # Remove the terminal from the set and remove the covering non-terminals
        terminals.remove(max_terminal)
        non_terminals -= max_coverage

    # Return the minimum set of non-terminals that cover all terminals
    return non_terminals


# Example usage
grammar = {
    'S': ['aSb', ''],
    'A': ['aA', 'b']
}

reynolds_cover = find_reynolds_cover(grammar)
print(f"Reynolds Cover: {reynolds_cover}")

