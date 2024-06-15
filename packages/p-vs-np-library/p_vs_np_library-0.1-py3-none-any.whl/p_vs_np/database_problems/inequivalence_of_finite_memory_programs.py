#Inequivalence of finite memory programs

def are_programs_inequivalent(program1, program2, memory_size):
    # Initialize memory for both programs
    memory1 = [0] * memory_size
    memory2 = [0] * memory_size

    # Execute the programs step by step and update memory
    for i in range(len(program1)):
        exec(program1[i], {'memory': memory1})
        exec(program2[i], {'memory': memory2})

    # Check if the memories of the programs are different
    if memory1 != memory2:
        return True

    return False

# Example usage
program1 = ["memory[0] = 1", "memory[1] = 2", "memory[2] = 3"]
program2 = ["memory[0] = 1", "memory[1] = 2", "memory[2] = 4"]
memory_size = 3

if are_programs_inequivalent(program1, program2, memory_size):
    print("Programs are inequivalent")
else:
    print("Programs are equivalent")
