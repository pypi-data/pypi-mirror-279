#Code Generation with Unfixed Variable Locations

class CodeGenerationWithUnfixedVariableLocations:
    def __init__(self, variables):
        self.variables = variables

    def generate_code(self):
        code = []

        for variable in self.variables:
            code.append(f"{variable} = allocate_memory()")

        return code

# Example usage
variables = ['x', 'y', 'z']

code_generator = CodeGenerationWithUnfixedVariableLocations(variables)
code = code_generator.generate_code()

print("Generated Code:")
for instruction in code:
    print(instruction)
