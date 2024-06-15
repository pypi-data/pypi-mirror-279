#Register Sufficiency For Loops







# Example usage





if __name__ == '__main__':
    class RegisterSufficiency:
        def __init__(self, program, loop_start, loop_end, num_registers):
            self.program = program
            self.loop_start = loop_start
            self.loop_end = loop_end
            self.num_registers = num_registers
        def is_register_sufficient(self):
            variable_registers = {}
            for i in range(self.loop_start, self.loop_end + 1):
                instruction = self.program[i]
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
    program = [
        ['ASSIGN', 'R1', 'R2'],
        ['ADD', 'R3', 'R1', 'R4'],
        ['SUB', 'R5', 'R6', 'R1'],
        ['ASSIGN', 'R7', 'R8'],
        ['MUL', 'R9', 'R7', 'R10']
    ]
    loop_start = 1
    loop_end = 3
    num_registers = 3
    sufficiency_checker = RegisterSufficiency(program, loop_start, loop_end, num_registers)
    result = sufficiency_checker.is_register_sufficient()
    print(f"Register Sufficiency for Loop: {result}")
