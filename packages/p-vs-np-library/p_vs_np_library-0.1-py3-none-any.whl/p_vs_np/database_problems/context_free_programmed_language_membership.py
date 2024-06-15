#Context Free Programmed Language Membership

def is_string_member(grammar, start_symbol, input_string):
    # Create a table to store the parsing results for substrings of the input string
    table = [[set() for _ in range(len(input_string))] for _ in range(len(input_string))]

    # Perform the CYK algorithm to fill in the parsing table
    for length in range(1, len(input_string) + 1):
        for i in range(len(input_string) - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for production in grammar:
                    for rule in grammar[production]:
                        if len(rule) == 2:
                            left, right = rule
                            if table[i][k] and table[k + 1][j] and right in table[i][k] and left in table[k + 1][j]:
                                table[i][j].add(production)

            for production in grammar:
                for rule in grammar[production]:
                    if len(rule) == 1 and rule == input_string[i: j + 1]:
                        table[i][j].add(production)

    # Check if the start symbol is present in the parsing results for the entire input string
    return start_symbol in table[0][len(input_string) - 1]


# Example usage
grammar = {
    'S': ['aS', 'bA'],
    'A': ['bA', '']
}

start_symbol = 'S'
input_string = 'abab'

is_member = is_string_member(grammar, start_symbol, input_string)
print(f"String Membership: {is_member}")
