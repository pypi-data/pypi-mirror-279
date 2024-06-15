#non-erasing stack automation acceptance












# Example usage
# Create the PDA and acceptance conditions



# Check if a string is accepted by the PDA

if __name__ == '__main__':
    class PDAState:
        def __init__(self, name):
            self.name = name
            self.transitions = []
        def add_transition(self, input_symbol, stack_symbol, next_state, stack_push):
            self.transitions.append((input_symbol, stack_symbol, next_state, stack_push))
        def get_transitions(self):
            return self.transitions
    class PDAAcceptance:
        def __init__(self, start_state, accepting_states):
            self.start_state = start_state
            self.accepting_states = accepting_states
        def is_accepted(self, input_string):
            stack = []
            current_state = self.start_state
            for symbol in input_string:
                transitions = current_state.get_transitions()
                found_transition = False
                for transition in transitions:
                    input_symbol, stack_symbol, next_state, stack_push = transition
                    if input_symbol == symbol and (not stack or stack[-1] == stack_symbol):
                        stack.pop()
                        if stack_push != '_':
                            stack.extend(stack_push[::-1])
                        current_state = next_state
                        found_transition = True
                        break
                if not found_transition:
                    return False
            return current_state in self.accepting_states
    q0 = PDAState('q0')
    q1 = PDAState('q1')
    q2 = PDAState('q2')
    q0.add_transition('0', '_', q1, 'A')
    q0.add_transition('1', 'A', q0, '_')
    q0.add_transition('1', '_', q2, '_')
    acceptance_conditions = PDAAcceptance(q0, {q2})
    input_string = '011'
    is_accepted = acceptance_conditions.is_accepted(input_string)
    print(f"Is the input string '{input_string}' accepted by the PDA? {is_accepted}")
