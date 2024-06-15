#Randomization test for matched pairs

import random

def randomization_test(matched_pairs):
    # Calculate the observed difference
    observed_diff = sum(x - y for x, y in matched_pairs)

    # Generate random permutations and calculate the difference for each permutation
    permutation_diffs = []
    num_permutations = 1000  # Number of random permutations to generate (adjust as needed)
    for _ in range(num_permutations):
        random.shuffle(matched_pairs)
        diff = sum(x - y for x, y in matched_pairs)
        permutation_diffs.append(diff)

    # Calculate the p-value
    num_extreme = sum(diff >= observed_diff for diff in permutation_diffs)
    p_value = (num_extreme + 1) / (num_permutations + 1)

    return observed_diff, p_value

# Example usage
if __name__ == '__main__':
    # Define your matched pairs as a list of tuples
    matched_pairs = [(2, 5), (4, 8), (3, 6), (1, 4), (7, 9)]

    # Run the randomization test
    observed_diff, p_value = randomization_test(matched_pairs)

    # Print the results
    print("Observed Difference:", observed_diff)
    print("p-value:", p_value)
