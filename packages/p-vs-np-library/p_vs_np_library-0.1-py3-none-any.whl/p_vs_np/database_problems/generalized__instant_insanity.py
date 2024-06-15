#Generalized  Instant Insanity

def solve_instant_insanity(cubes):
    # Solve the Instant Insanity puzzle

    # Base case: all cubes have been placed
    if len(cubes) == 0:
        return cubes

    cube = cubes[0]

    # Try all possible orientations for the current cube
    for orientation in range(4):
        if can_place_cube(cube, orientation):
            place_cube(cube, orientation)
            result = solve_instant_insanity(cubes[1:])
            if result is not None:
                return result
            remove_cube(cube, orientation)

    return None  # No solution found


def can_place_cube(cube, orientation):
    # Check if it is possible to place the cube in the current orientation

    # Check if any of the faces of the cube conflict with the previously placed cubes
    for i in range(len(cube)):
        if cube[i] in placed_faces[i]:
            return False

    return True


def place_cube(cube, orientation):
    # Place the cube in the current orientation

    # Add the faces of the cube to the placed_faces list
    for i in range(len(cube)):
        placed_faces[i].add(cube[i])


def remove_cube(cube, orientation):
    # Remove the cube from the placed_faces list

    # Remove the faces of the cube from the placed_faces list
    for i in range(len(cube)):
        placed_faces[i].remove(cube[i])


# Example usage
cubes = [
    ["red", "blue", "green", "yellow"],
    ["red", "yellow", "blue", "green"],
    ["yellow", "red", "green", "blue"],
    ["green", "blue", "red", "yellow"]
]

# Initialize the placed_faces list
placed_faces = [set() for _ in range(len(cubes[0]))]

solution = solve_instant_insanity(cubes)

if solution is not None:
    print("Instant Insanity solution:")
    for cube in solution:
        print(cube)
else:
    print("No solution found.")
