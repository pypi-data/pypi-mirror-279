#Inequivalence of finite memory programs

    # Initialize memory for both programs

    # Execute the programs step by step and update memory

    # Check if the memories of the programs are different


# Example usage


if __name__ == '__main__':
    def are_programs_inequivalent(program1, program2, memory_size):
        memory1 = [0] * memory_size
        memory2 = [0] * memory_size
        for i in range(len(program1)):
            exec(program1[i], {'memory': memory1})
            exec(program2[i], {'memory': memory2})
        if memory1 != memory2:
            return True
        return False
    program1 = ["memory[0] = 1", "memory[1] = 2", "memory[2] = 3"]
    program2 = ["memory[0] = 1", "memory[1] = 2", "memory[2] = 4"]
    memory_size = 3
    if are_programs_inequivalent(program1, program2, memory_size):
        print("Programs are inequivalent")
    else:
        print("Programs are equivalent")
