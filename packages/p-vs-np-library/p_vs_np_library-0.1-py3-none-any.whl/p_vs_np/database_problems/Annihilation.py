#Annihilation


def find_annihilation_subset(numbers):
    def backtrack(curr_subset, curr_sum, start):
        if curr_sum == 0:
            return curr_subset

        for i in range(start, len(numbers)):
            num = numbers[i]

            # Add the number to the current subset
            curr_subset.append(num)
            curr_sum += num

            # Recursively explore the next numbers
            result = backtrack(curr_subset, curr_sum, i + 1)

            if result is not None:
                return result

            # Remove the number from the current subset
            curr_subset.pop()
            curr_sum -= num

        return None

    subset = []
    result = backtrack(subset, 0, 0)
    return result


# Example usage
numbers = [2, -3, 1, 5, -4]
annihilation_subset = find_annihilation_subset(numbers)

if annihilation_subset is not None:
    print("Subset that sums to zero:", annihilation_subset)
else:
    print("No subset found that sums to zero.")

