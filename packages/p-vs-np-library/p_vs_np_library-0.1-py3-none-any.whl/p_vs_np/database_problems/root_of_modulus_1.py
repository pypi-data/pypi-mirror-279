#root of modulus 1

import cmath

def is_root_of_modulus_1(z):
    modulus = abs(z)
    return abs(modulus - 1) < 1e-9  # Check if the modulus is close to 1

# Example usage
z1 = cmath.exp(1j * 0.5 * cmath.pi)  # Complex number e^(i * pi / 6)
z2 = cmath.exp(1j * cmath.pi)       # Complex number e^(i * pi)

print("Is z1 a root of modulus 1?", is_root_of_modulus_1(z1))
print("Is z2 a root of modulus 1?", is_root_of_modulus_1(z2))

