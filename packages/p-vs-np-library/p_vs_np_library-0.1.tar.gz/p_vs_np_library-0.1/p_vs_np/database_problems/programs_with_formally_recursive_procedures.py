#Programs with formally recursive procedures

import re

def is_formally_recursive(program):
    # Parse procedure declarations
    pattern = r'procedure\s+(\w+)\('
    procedure_declarations = re.findall(pattern, program)

    # Parse procedure calls
    pattern = r'\b(\w+)\('
    procedure_calls = re.findall(pattern, program)

    # Check if any procedure is formally recursive
    for procedure in procedure_declarations:
        if procedure in procedure_calls:
            return True

    return False

# Example usage
program = """
procedure foo()
    bar()
end

procedure bar()
    foo()
end

procedure baz()
    qux()
end

procedure qux()
    print("Hello!")
end
"""

if is_formally_recursive(program):
    print("The program contains formally recursive procedures.")
else:
    print("The program does not contain formally recursive procedures.")

