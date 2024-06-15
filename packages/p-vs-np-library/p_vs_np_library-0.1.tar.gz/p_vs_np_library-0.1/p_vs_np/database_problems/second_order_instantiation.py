#Second Order Instantiation

class Expression:
    def __init__(self, variables, functions):
        self.variables = variables
        self.functions = functions

    def substitute(self, substitution):
        substituted_variables = [substitution.get(var, var) for var in self.variables]
        substituted_functions = [function.substitute(substitution) for function in self.functions]
        return Expression(substituted_variables, substituted_functions)

    def is_identical(self, target):
        return self.variables == target.variables and self.functions == target.functions


class Function:
    def __init__(self, symbol, arguments):
        self.symbol = symbol
        self.arguments = arguments

    def substitute(self, substitution):
        substituted_arguments = [arg.substitute(substitution) if isinstance(arg, Expression) else substitution.get(arg, arg)
                                 for arg in self.arguments]
        return Function(self.symbol, substituted_arguments)


def second_order_instantiation(expression1, expression2, substitution):
    substituted_expression1 = expression1.substitute(substitution)
    return substituted_expression1.is_identical(expression2)


# Example usage
# Define the expressions and substitution
E_base1 = Expression(['x', 'y'], [Function('f', ['x']), Function('g', ['y'])])
E_base2 = Expression([], [Function('h', [])])
substitution = {'x': Function('h', []), 'y': Function('g', [])}

# Call the second_order_instantiation function
result = second_order_instantiation(E_base1, E_base2, substitution)
print(f"Is there a substitution that makes E_base1 identical to E_base2? {result}")
