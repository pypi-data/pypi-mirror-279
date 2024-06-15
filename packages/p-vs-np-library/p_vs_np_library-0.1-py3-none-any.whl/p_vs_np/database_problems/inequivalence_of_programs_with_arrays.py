#Inequivalence of programs with arrays

def are_programs_inequivalent(program1, program2):
    # Check if the programs have different lengths
    if len(program1) != len(program2):
        return True

    # Check if the programs access different array elements
    for i in range(len(program1)):
        if program1[i] != program2[i]:
            return True

    return False

# Example usage
program1 = ["array[0] = 1", "array[1] = 2", "array[2] = 3"]
program2 = ["array[0] = 1", "array[1] = 2", "array[3] = 3"]

if are_programs_inequivalent(program1, program2):
    print("Programs are inequivalent")
else:
    print("Programs are equivalent")
