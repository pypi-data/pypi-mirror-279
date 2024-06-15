#Code Generation on a One-Register Machine

class OneRegisterCodeGeneration:
    def __init__(self, input_value, output_value):
        self.input_value = input_value
        self.output_value = output_value

    def generate_code(self):
        code = []
        current_value = self.input_value

        while current_value != self.output_value:
            if current_value % 2 == 0:
                code.append('INC')
                current_value += 1
            else:
                code.append('DEC')
                current_value -= 1

        return code

# Example usage
input_value = 5
output_value = 10

code_generator = OneRegisterCodeGeneration(input_value, output_value)
code = code_generator.generate_code()

print("Generated Code:")
for instruction in code:
    print(instruction)
