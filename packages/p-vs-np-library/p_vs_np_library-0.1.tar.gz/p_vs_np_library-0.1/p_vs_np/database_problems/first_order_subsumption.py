#First Order Subsumption

class Expression:
    def __init__(self, variables, functions):
        self.variables = variables
        self.functions = functions

    def substitute(self, substitution):
        substituted_variables = [substitution.get(var, var) for var in self.variables]
        substituted_functions = [function.substitute(substitution) for function in self.functions]
        return Expression(substituted_variables, substituted_functions)

    def is_subsumed(self, target):
        if len(self.variables) != len(target.variables):
            return False

        for func1, func2 in zip(self.functions, target.functions):
            if not func1.is_subsumed(func2):
                return False

        return True


class Function:
    def __init__(self, symbol, arguments):
        self.symbol = symbol
        self.arguments = arguments

    def substitute(self, substitution):
        substituted_arguments = [arg.substitute(substitution) if isinstance(arg, Expression) else substitution.get(arg, arg)
                                 for arg in self.arguments]
        return Function(self.symbol, substituted_arguments)

    def is_subsumed(self, target):
        if self.symbol != target.symbol:
            return False

        if len(self.arguments) != len(target.arguments):
            return False

        for arg1, arg2 in zip(self.arguments, target.arguments):
            if isinstance(arg1, Expression):
                if not arg1.is_subsumed(arg2):
                    return False
            elif arg1 != arg2:
                return False

        return True


def first_order_subsumption(expressions, targets, substitution):
    if not expressions:
        return True

    current_expression = expressions[0]
    remaining_expressions = expressions[1:]

    for target in targets:
        if current_expression.is_subsumed(target.substitute(substitution)):
            if first_order_subsumption(remaining_expressions, targets, substitution):
                return True

    return False


# Example usage
# Define the expressions and targets
U = {'x', 'y'}
C = {'f', 'g', 'h'}
E_base = [
    Expression(['x'], [Function('f', ['x'])]),
    Expression(['x', 'y'], [Function('g', ['x', 'y'])]),
    Expression(['y'], [Function('h', ['y'])])
]
F_base = [
    Expression([], [Function('f', ['x'])]),
    Expression(['y'], [Function('g', ['y', 'y'])])
]

# Call the first_order_subsumption function
result = first_order_subsumption(E_base, F_base, {'x': Function('g', ['y', 'h(y)']), 'y': 'z'})
print(f"Does there exist a substitution mapping? {result}")
