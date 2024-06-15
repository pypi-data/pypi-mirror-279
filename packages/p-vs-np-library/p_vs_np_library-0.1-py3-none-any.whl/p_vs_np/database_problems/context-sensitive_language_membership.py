#Context-Sensitive Language Membership

class ContextSensitiveAutomaton:
    def __init__(self, start_state, transitions):
        self.start_state = start_state
        self.transitions = transitions

    def is_string_member(self, input_string):
        tape = ['#'] + list(input_string) + ['#']  # Add boundary symbols to the input string
        current_state = self.start_state
        tape_index = 1

        while True:
            if (current_state, tape[tape_index]) in self.transitions:
                next_state, write_symbol, direction = self.transitions[(current_state, tape[tape_index])]
                tape[tape_index] = write_symbol
                current_state = next_state

                if direction == 'L':
                    tape_index -= 1
                elif direction == 'R':
                    tape_index += 1

            elif current_state in self.transitions:
                next_state, write_symbol, direction = self.transitions[current_state]

                if next_state is None:
                    return True  # Reached an accepting state

                tape[tape_index] = write_symbol
                current_state = next_state

                if direction == 'L':
                    tape_index -= 1
                elif direction == 'R':
                    tape_index += 1

            else:
                return False  # No transition defined for the current state and tape symbol

# Example usage
start_state = 'S'
transitions = {
    ('S', '#'): ('A', '#', 'R'),
    ('A', '0'): ('B', 'X', 'R'),
    ('B', '0'): ('B', '0', 'R'),
    ('B', '#'): ('C', '#', 'L'),
    ('C', 'X'): ('C', 'X', 'L'),
    ('C', '0'): ('C', '0', 'L'),
    ('C', '#'): ('D', '#', 'R'),
    ('D', 'X'): ('D', 'X', 'R'),
    ('D', '#'): ('E', '#', 'R'),
    ('E', 'X'): ('E', 'X', 'R'),
    ('E', '#'): ('F', '#', 'L'),
    ('F', '0'): ('G', 'X', 'L'),
    ('G', '0'): ('G', '0', 'L'),
    ('G', '#'): ('H', '#', 'R'),
    ('H', 'X'): ('H', 'X', 'R'),
    ('H', '#'): (None, '#', 'R')  # Accepting state
}

automaton = ContextSensitiveAutomaton(start_state, transitions)

input_string = '000'

is_member = automaton.is_string_member(input_string)
print(f"String Membership: {is_member}")
