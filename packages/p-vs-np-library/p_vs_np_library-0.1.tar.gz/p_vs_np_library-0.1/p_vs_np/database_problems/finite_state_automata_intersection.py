#Finite State Automata Intersection

class FSA:
    def __init__(self, states, alphabet, transitions, start_state, accepting_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accepting_states = accepting_states

    def is_intersection_empty(self, other_fsa):
        intersection_states = set()
        intersection_accepting_states = set()

        for state1 in self.states:
            for state2 in other_fsa.states:
                intersection_states.add((state1, state2))
                if state1 in self.accepting_states and state2 in other_fsa.accepting_states:
                    intersection_accepting_states.add((state1, state2))

        visited = set()
        stack = [(self.start_state, other_fsa.start_state)]

        while stack:
            current_state = stack.pop()
            visited.add(current_state)

            for symbol in self.alphabet:
                next_state1 = self.transitions.get((current_state[0], symbol))
                next_state2 = other_fsa.transitions.get((current_state[1], symbol))

                if next_state1 is not None and next_state2 is not None:
                    if (next_state1, next_state2) not in visited:
                        stack.append((next_state1, next_state2))

        return bool(intersection_accepting_states.intersection(visited))

# Example usage
# Create the FSAs
fsa1_states = {'q0', 'q1', 'q2'}
fsa1_alphabet = {'0', '1'}
fsa1_transitions = {('q0', '0'): 'q1', ('q1', '1'): 'q2', ('q2', '0'): 'q0'}
fsa1_start_state = 'q0'
fsa1_accepting_states = {'q2'}

fsa2_states = {'p0', 'p1', 'p2'}
fsa2_alphabet = {'0', '1'}
fsa2_transitions = {('p0', '0'): 'p1', ('p1', '1'): 'p2', ('p2', '0'): 'p0'}
fsa2_start_state = 'p0'
fsa2_accepting_states = {'p1'}

fsa1 = FSA(fsa1_states, fsa1_alphabet, fsa1_transitions, fsa1_start_state, fsa1_accepting_states)
fsa2 = FSA(fsa2_states, fsa2_alphabet, fsa2_transitions, fsa2_start_state, fsa2_accepting_states)

# Check if the intersection of the FSAs is empty
is_intersection_empty = fsa1.is_intersection_empty(fsa2)
print(f"Is the intersection of the FSAs empty? {is_intersection_empty}")

