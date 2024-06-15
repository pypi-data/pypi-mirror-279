#Code Generation with Unlimited Registers



        # Move the input value to the first register

                # Increment the current register until it reaches the target register
                # Decrement the current register until it reaches the target register

        # Move the value in the target register to the output


# Example usage



if __name__ == '__main__':
    class UnlimitedRegisterCodeGeneration:
        def __init__(self, input_value, output_value):
            self.input_value = input_value
            self.output_value = output_value
        def generate_code(self):
            code = []
            current_register = 0
            target_register = 1
            code.append(f"MOV {self.input_value} R{current_register}")
            while current_register != target_register:
                if current_register < target_register:
                    code.append(f"INC R{current_register}")
                    current_register += 1
                else:
                    code.append(f"DEC R{current_register}")
                    current_register -= 1
            code.append(f"MOV R{target_register} OUTPUT")
            return code
    input_value = 5
    output_value = 10
    code_generator = UnlimitedRegisterCodeGeneration(input_value, output_value)
    code = code_generator.generate_code()
    print("Generated Code:")
    for instruction in code:
        print(instruction)
