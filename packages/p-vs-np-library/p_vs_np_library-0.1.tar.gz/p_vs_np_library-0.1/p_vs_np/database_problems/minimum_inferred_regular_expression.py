#Minimum Inferred Regular Expression

import regex as re


def find_minimum_regular_expression(strings):
    # Create a regex pattern by joining all strings with '|'
    regex_pattern = '|'.join(strings)

    # Find the minimum regular expression using the `re.compile` function
    regex = re.compile(regex_pattern)

    # Return the pattern of the minimum regular expression
    return regex.pattern


# Example usage
strings = ['abc', 'abd', 'acd']

minimum_regex = find_minimum_regular_expression(strings)
print(f"Minimum Regular Expression: {minimum_regex}")
