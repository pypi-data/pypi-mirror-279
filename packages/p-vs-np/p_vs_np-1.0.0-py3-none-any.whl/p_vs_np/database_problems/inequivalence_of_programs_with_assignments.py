#Inequivalence of Programs with Assignments

    # Check if the programs have different lengths

    # Check if the programs have different assignments


# Example usage


if __name__ == '__main__':
    def are_programs_inequivalent(program1, program2):
        if len(program1) != len(program2):
            return True
        for i in range(len(program1)):
            if program1[i] != program2[i]:
                return True
        return False
    program1 = ["x = 1", "y = 2", "z = 3"]
    program2 = ["x = 1", "y = 2", "z = 4"]
    if are_programs_inequivalent(program1, program2):
        print("Programs are inequivalent")
    else:
        print("Programs are equivalent")
