#Quasi-Realtime Automation Acceptance

class QuasiRealtimeAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accepting_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accepting_states = accepting_states

    def accepts(self, string):
        current_state = self.start_state
        time = 0

        for symbol in string:
            transition = self.transitions.get((current_state, symbol), None)

            if transition is None:
                return False

            new_state, output, duration = transition
            current_state = new_state
            time += duration

            if time > len(string):
                return False

            if output != symbol:
                return False

        return current_state in self.accepting_states


# Example usage
# Define a quasi-realtime automaton
qra = QuasiRealtimeAutomaton(
    states={'q0', 'q1', 'q2'},
    alphabet={'0', '1'},
    transitions={
        ('q0', '0'): ('q1', '0', 2),
        ('q1', '1'): ('q2', '1', 1),
        ('q2', '0'): ('q0', '0', 3)
    },
    start_state='q0',
    accepting_states={'q2'}
)

# Check if the automaton accepts a specific input string
result = qra.accepts("010")
print(f"Does the automaton accept the input string? {result}")


