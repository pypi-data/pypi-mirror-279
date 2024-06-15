#Hitting String

def find_hitting_string(A, n):
    # Generate all possible strings of length n
    all_strings = generate_all_strings(n)

    # Check each string to see if it covers all elements in A
    for string in all_strings:
        if covers_all_elements(string, A):
            return string

    return None  # No hitting string found

def generate_all_strings(n):
    all_strings = []

    def backtrack(string, length):
        if length == 0:
            all_strings.append(string)
        else:
            backtrack(string + '0', length - 1)
            backtrack(string + '1', length - 1)

    backtrack('', n)
    return all_strings

def covers_all_elements(string, A):
    for element in A:
        if not contains_element(string, element):
            return False
    return True

def contains_element(string, element):
    n = len(string)
    for i in range(n):
        if string[i] == element[i]:
            return True
    return False

# Example usage
A = ['010', '001', '101']
n = 3

result = find_hitting_string(A, n)
if result:
    print("Hitting String:", result)
else:
    print("No hitting string found.")

