#Linear Bounded Automation Acceptance









# Example usage
# Define a linear bounded automaton

# Check if the automaton accepts a specific input string

if __name__ == '__main__':
    class LinearBoundedAutomaton:
        def __init__(self, states, alphabet, transitions, start_state, accepting_states):
            self.states = states
            self.alphabet = alphabet
            self.transitions = transitions
            self.start_state = start_state
            self.accepting_states = accepting_states
        def accepts(self, string):
            tape = ['#'] + list(string) + ['#']
            current_state = self.start_state
            head_position = 1
            while current_state not in self.accepting_states:
                symbol = tape[head_position]
                transition = self.transitions[current_state].get(symbol, None)
                if transition is None:
                    return False
                new_state, new_symbol, movement = transition
                tape[head_position] = new_symbol
                current_state = new_state
                if movement == 'L':
                    if head_position == 0:
                        tape = ['#'] + tape
                    else:
                        head_position -= 1
                elif movement == 'R':
                    head_position += 1
                    if head_position == len(tape):
                        tape.append('#')
            return True
    lba = LinearBoundedAutomaton(
        states={'q0', 'q1', 'q2'},
        alphabet={'0', '1'},
        transitions={
            'q0': {'0': ('q1', '0', 'R'), '1': ('q2', '1', 'R')},
            'q1': {'0': ('q1', '0', 'R'), '1': ('q1', '1', 'R')},
            'q2': {'1': ('q2', '1', 'R')}
        },
        start_state='q0',
        accepting_states={'q2'}
    )
    result = lba.accepts("0000111")
    print(f"Does the automaton accept the input string? {result}")
