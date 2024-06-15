#Two way Finite State Automation Non-Emptiness










# Example usage
# Define a two-way finite state automaton

# Check if the automaton accepts any input string

if __name__ == '__main__':
    class TwoWayFiniteStateAutomaton:
        def __init__(self, states, alphabet, transitions, start_state, accepting_states):
            self.states = states
            self.alphabet = alphabet
            self.transitions = transitions
            self.start_state = start_state
            self.accepting_states = accepting_states
        def accepts(self, string):
            current_state = self.start_state
            head_position = 0
            while True:
                if current_state in self.accepting_states:
                    return True
                if head_position < 0 or head_position >= len(string):
                    return False
                symbol = string[head_position]
                direction = self.transitions[current_state].get(symbol, None)
                if direction is None:
                    return False
                new_state, movement = direction
                current_state = new_state
                if movement == 'L':
                    head_position -= 1
                elif movement == 'R':
                    head_position += 1
    fsa = TwoWayFiniteStateAutomaton(
        states={'q0', 'q1', 'q2'},
        alphabet={'0', '1'},
        transitions={
            'q0': {'0': ('q1', 'R'), '1': ('q2', 'R')},
            'q1': {'0': ('q0', 'R'), '1': ('q1', 'L')},
            'q2': {'0': ('q2', 'R'), '1': ('q1', 'L')}
        },
        start_state='q0',
        accepting_states={'q0'}
    )
    result = fsa.accepts("1010101")
    print(f"Does the automaton accept any input string? {result}")
