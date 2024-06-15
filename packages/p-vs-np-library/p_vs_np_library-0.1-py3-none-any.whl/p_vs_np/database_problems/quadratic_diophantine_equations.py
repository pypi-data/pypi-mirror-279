#Quadratic diophantine equations

def solve_quadratic_diophantine(a, b, c, d, e, f):
    # Check if the equation is linear
    if a == 0 and b == 0 and c == 0:
        if d == 0 and e == 0 and f == 0:
            return True  # Infinite integer solutions
        else:
            return False  # No integer solutions

    # Check if the equation is homogeneous
    if d == 0 and e == 0 and f == 0:
        return True  # Infinite integer solutions

    # Solve the equation using a loop
    for x in range(-100, 101):
        for y in range(-100, 101):
            if a * x**2 + b * x * y + c * y**2 + d * x + e * y + f == 0:
                return True  # Integer solution found

    return False  # No integer solutions found

# Example usage
a = 2
b = 1
c = 3
d = 4
e = 5
f = 6

has_integer_solution = solve_quadratic_diophantine(a, b, c, d, e, f)
print("Has integer solution:", has_integer_solution)
