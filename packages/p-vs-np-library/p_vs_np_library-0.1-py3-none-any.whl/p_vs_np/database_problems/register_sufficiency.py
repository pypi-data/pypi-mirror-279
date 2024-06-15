#Register Sufficiency

class RegisterSufficiency:
    def __init__(self, program, num_registers):
        self.program = program
        self.num_registers = num_registers

    def is_sufficient_registers(self):
        used_registers = set()
        for instruction in self.program:
            for operand in instruction[1:]:
                if operand.startswith('R'):
                    used_registers.add(operand)

            if len(used_registers) > self.num_registers:
                return False

        return True

# Example usage
program1 = [
    ['ADD', 'R1', 'R2', 'R3'],
    ['SUB', 'R4', 'R5', 'R6'],
    ['MUL', 'R7', 'R8', 'R9']
]

program2 = [
    ['ADD', 'R1', 'R2', 'R3'],
    ['SUB', 'R4', 'R5', 'R6'],
    ['MUL', 'R7', 'R8', 'R9'],
    ['DIV', 'R10', 'R11', 'R12']
]

num_registers = 5

sufficiency_checker1 = RegisterSufficiency(program1, num_registers)
sufficiency_checker2 = RegisterSufficiency(program2, num_registers)

result1 = sufficiency_checker1.is_sufficient_registers()
result2 = sufficiency_checker2.is_sufficient_registers()

print(f"Program 1 Register Sufficiency: {result1}")
print(f"Program 2 Register Sufficiency: {result2}")
