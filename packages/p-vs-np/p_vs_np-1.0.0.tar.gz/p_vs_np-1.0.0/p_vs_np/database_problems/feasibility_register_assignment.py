#Feasibility Register Assignment







# Example usage






if __name__ == '__main__':
    class RegisterAssignment:
        def __init__(self, program, num_registers):
            self.program = program
            self.num_registers = num_registers
        def is_feasible_assignment(self):
            variable_registers = {}
            for instruction in self.program:
                operation, destination, *operands = instruction
                if destination.startswith('R'):
                    variable_registers[destination] = destination
                for operand in operands:
                    if operand.startswith('R'):
                        if operand not in variable_registers:
                            return False
                if operation == 'ASSIGN':
                    source = operands[0]
                    variable_registers[destination] = variable_registers[source]
            return True
    program1 = [
        ['ASSIGN', 'R1', 'R2'],
        ['ADD', 'R3', 'R1', 'R4'],
        ['SUB', 'R5', 'R6', 'R1']
    ]
    program2 = [
        ['ASSIGN', 'R1', 'R2'],
        ['ADD', 'R3', 'R1', 'R4'],
        ['SUB', 'R5', 'R6', 'R7']
    ]
    num_registers = 3
    assignment_checker1 = RegisterAssignment(program1, num_registers)
    assignment_checker2 = RegisterAssignment(program2, num_registers)
    result1 = assignment_checker1.is_feasible_assignment()
    result2 = assignment_checker2.is_feasible_assignment()
    print(f"Program 1 Register Assignment Feasibility: {result1}")
    print(f"Program 2 Register Assignment Feasibility: {result2}")
