#Minimum Inferred Finite State Automation

from collections import deque


class FSA:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.start_state = None
        self.accepting_states = set()

    def add_transition(self, state, symbol, next_state):
        self.states.add(state)
        self.states.add(next_state)
        self.alphabet.add(symbol)
        self.transitions[(state, symbol)] = next_state

    def set_start_state(self, start_state):
        self.start_state = start_state
        self.states.add(start_state)

    def add_accepting_state(self, state):
        self.accepting_states.add(state)

    def infer_minimum_dfa(self, strings):
        # Create a queue for BFS traversal
        queue = deque([frozenset(self.accepting_states)])
        visited = set([frozenset(self.accepting_states)])

        while queue:
            current_states = queue.popleft()

            for symbol in self.alphabet:
                next_states = set()

                for state in current_states:
                    if (state, symbol) in self.transitions:
                        next_state = self.transitions[(state, symbol)]
                        next_states.add(next_state)

                if not next_states:
                    continue

                if next_states not in visited:
                    visited.add(next_states)
                    queue.append(next_states)

                    for string in strings:
                        if not self.is_accepted(string, next_states):
                            break
                    else:
                        return FSA.from_states(next_states)

        return None

    def is_accepted(self, string, states=None):
        if states is None:
            states = {self.start_state}

        for symbol in string:
            next_states = set()

            for state in states:
                if (state, symbol) in self.transitions:
                    next_state = self.transitions[(state, symbol)]
                    next_states.add(next_state)

            if not next_states:
                return False

            states = next_states

        return any(state in self.accepting_states for state in states)

    @classmethod
    def from_states(cls, states):
        fsa = cls()

        for state in states:
            fsa.states.add(state)

            if state in fsa.accepting_states:
                fsa.add_accepting_state(state)

        return fsa


# Example usage
strings = ["ab", "bb", "baa", "aba", "aab", "aaab"]

# Create the initial FSA
fsa = FSA()
fsa.add_transition('q0', 'a', 'q1')
fsa.add_transition('q0', 'b', 'q2')
fsa.add_transition('q1', 'a', 'q2')
fsa.add_transition('q1', 'b', 'q0')
fsa.add_transition('q2', 'a', 'q2')
fsa.add_transition('q2', 'b', 'q2')
fsa.set_start_state('q0')
fsa.add_accepting_state('q2')

# Infer the minimum DFA
minimum_dfa = fsa.infer_minimum_dfa(strings)

# Print the inferred minimum DFA
if minimum_dfa:
    print("Minimum DFA:")
    print("States:", minimum_dfa.states)
    print("Alphabet:", minimum_dfa.alphabet)
    print("Transitions:", minimum_dfa.transitions)
    print("Start state:", minimum_dfa.start_state)
    print("Accepting states:", minimum_dfa.accepting_states)
else:
    print("No minimum DFA found.")
