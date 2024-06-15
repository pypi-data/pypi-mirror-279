#Composite Number

import math

def is_composite_number(n):
    if n < 2:
        return False

    # Check divisibility up to the square root of n
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return True

    return False

# Example usage
if __name__ == '__main__':
    # Example number
    number = 15

    # Check if the number is composite
    result = is_composite_number(number)

    # Print the result
    if result:
        print(f"The number {number} is composite.")
    else:
        print(f"The number {number} is not composite.")

