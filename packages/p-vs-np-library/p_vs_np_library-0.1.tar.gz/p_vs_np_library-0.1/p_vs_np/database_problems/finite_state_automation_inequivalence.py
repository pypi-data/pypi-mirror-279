#Finite State Automation Inequivalence

class FiniteStateAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accepting_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accepting_states = accepting_states

    def accepts(self, string):
        current_state = self.start_state
        for char in string:
            if char not in self.alphabet:
                return False
            current_state = self.transitions[current_state].get(char)
            if current_state is None:
                return False
        return current_state in self.accepting_states


def is_inequivalent(fsa1, fsa2):
    # Check if the sets of accepting states are different
    if set(fsa1.accepting_states) != set(fsa2.accepting_states):
        return True

    # Check if there exists a string that is accepted by one automaton but not the other
    for string in generate_strings(fsa1.alphabet):
        if fsa1.accepts(string) != fsa2.accepts(string):
            return True

    return False


def generate_strings(alphabet):
    yield ""
    for string_length in range(1, 10):  # Generate strings of length up to 10
        for string in product(alphabet, repeat=string_length):
            yield "".join(string)


# Example usage
# Define two finite state automata
fsa1 = FiniteStateAutomaton(
    states={'q0', 'q1'},
    alphabet={'0', '1'},
    transitions={'q0': {'0': 'q1', '1': 'q0'}, 'q1': {'0': 'q0', '1': 'q1'}},
    start_state='q0',
    accepting_states={'q0'}
)

fsa2 = FiniteStateAutomaton(
    states={'q0', 'q1', 'q2'},
    alphabet={'0', '1'},
    transitions={'q0': {'0': 'q1', '1': 'q2'}, 'q1': {'0': 'q1', '1': 'q0'}, 'q2': {'0': 'q0', '1': 'q2'}},
    start_state='q0',
    accepting_states={'q0', 'q2'}
)

# Check if the automata are inequivalent
result = is_inequivalent(fsa1, fsa2)
print(f"Are the automata inequivalent? {result}")

