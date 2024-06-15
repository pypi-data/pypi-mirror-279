#Quasi-Real Time Language Membership






# Example usage





if __name__ == '__main__':
    class QuasiRealTimeAutomaton:
        def __init__(self, states, alphabet, transitions, start_state, accept_states):
            self.states = states
            self.alphabet = alphabet
            self.transitions = transitions
            self.start_state = start_state
            self.accept_states = accept_states
        def is_string_member(self, input_string):
            current_state = self.start_state
            for symbol in input_string:
                if (current_state, symbol) in self.transitions:
                    current_state = self.transitions[(current_state, symbol)]
                else:
                    return False
            return current_state in self.accept_states
    states = {'q0', 'q1', 'q2'}
    alphabet = {'a', 'b'}
    transitions = {('q0', 'a'): 'q1', ('q1', 'b'): 'q2'}
    start_state = 'q0'
    accept_states = {'q2'}
    automaton = QuasiRealTimeAutomaton(states, alphabet, transitions, start_state, accept_states)
    input_string = 'ab'
    is_member = automaton.is_string_member(input_string)
    print(f"String Membership: {is_member}")
