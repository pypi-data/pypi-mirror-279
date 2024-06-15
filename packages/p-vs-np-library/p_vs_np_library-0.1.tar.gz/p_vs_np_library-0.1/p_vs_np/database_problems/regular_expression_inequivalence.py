#Regular Expression Inequivalence

import re


def are_regular_expressions_inequivalent(regex1, regex2):
    # Add anchors to the regular expressions to match the entire string
    regex1 = f"^{regex1}$"
    regex2 = f"^{regex2}$"

    # Generate a sample of strings to test
    sample_strings = generate_sample_strings()

    # Check if the regular expressions match the same strings
    for string in sample_strings:
        if re.match(regex1, string) != re.match(regex2, string):
            return True

    return False


def generate_sample_strings():
    # Customize this function to generate sample strings for testing
    return ["", "a", "abc", "aaa", "bb", "cd", "xyz"]


# Example usage
regex1 = "(ab)*"
regex2 = "a(ba)*"

if are_regular_expressions_inequivalent(regex1, regex2):
    print("The regular expressions are inequivalent.")
else:
    print("The regular expressions are equivalent.")

