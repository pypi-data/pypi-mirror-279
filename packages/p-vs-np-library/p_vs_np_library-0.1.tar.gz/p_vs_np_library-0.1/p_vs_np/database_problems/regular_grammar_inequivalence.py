#Regular Grammar Inequivalence

def are_regular_grammars_inequivalent(grammar1, grammar2):
    # Generate the languages for both grammars
    language1 = generate_language(grammar1)
    language2 = generate_language(grammar2)

    # Check if the languages are different
    if language1 != language2:
        return True
    else:
        return False


def generate_language(grammar):
    # Initialize the language as an empty set
    language = set()

    # Iterate through each production rule
    for non_terminal, productions in grammar.items():
        for production in productions:
            # Generate the words by expanding the production rules
            words = generate_words(grammar, production)

            # Add the generated words to the language
            language.update(words)

    return language


def generate_words(grammar, production):
    # Base case: If the production is empty, return an empty word
    if production == '':
        return ['']

    words = []

    # Expand the non-terminals in the production
    for symbol in production:
        if symbol in grammar:
            non_terminal_productions = grammar[symbol]

            # Recursively generate words for each non-terminal
            non_terminal_words = generate_words(grammar, non_terminal_productions[0])

            # Concatenate the generated words with the remaining production
            words = [word + remaining for word in non_terminal_words for remaining in generate_words(grammar, production[1:])]

        else:
            # The symbol is a terminal, so append it to each word
            words = [word + symbol for word in words]

    return words


# Example usage
grammar1 = {
    'S': ['aS', 'bA', ''],
    'A': ['aA', 'bB'],
    'B': ['bB', 'b']
}

grammar2 = {
    'S': ['aS', 'bS', ''],
    'A': ['aA', 'bB'],
    'B': ['bB', 'b']
}

inequivalent = are_regular_grammars_inequivalent(grammar1, grammar2)
print(f"Inequivalent: {inequivalent}")

