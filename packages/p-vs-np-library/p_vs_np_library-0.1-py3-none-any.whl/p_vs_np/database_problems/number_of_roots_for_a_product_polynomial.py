#number of roots for a product polynomial

import numpy as np

def count_roots(product_polynomial):
    # Convert the product polynomial to a list of coefficients
    coefficients = list(product_polynomial)

    # Use numpy's roots function to calculate the roots of the polynomial
    roots = np.roots(coefficients)

    # Count the number of distinct roots
    num_roots = len(set(roots))

    return num_roots

# Example usage
polynomial = [1, -3, 2]  # Represents the polynomial (x-1)(x-2)

num_roots = count_roots(polynomial)

print("Number of roots:", num_roots)

