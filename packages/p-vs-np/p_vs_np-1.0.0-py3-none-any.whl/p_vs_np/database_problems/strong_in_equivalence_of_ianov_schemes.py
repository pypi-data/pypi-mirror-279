#Strong in equivalence of ianov schemes




# Define the functions and predicates
    # Define other functions

    # Define other predicates

# Define the domain set D

# Define the two ianov schemes


# Check for strong inequivalence

if __name__ == '__main__':
    def evaluate_instruction(instruction, functions, predicates, x):
        if instruction.startswith("x <---"):
            func_name = instruction.split("<---")[1].strip()
            if func_name in functions:
                return functions[func_name](x)
        elif instruction.startswith("if"):
            predicate_name = instruction.split("if")[1].split("then")[0].strip()
            if predicate_name in predicates:
                return predicates[predicate_name](x)
        elif instruction.strip() == "halt":
            return None
    def simulate_scheme(instructions, functions, predicates, x):
        pc = 0
        while pc < len(instructions):
            instruction = instructions[pc]
            result = evaluate_instruction(instruction, functions, predicates, x)
            if result is None:
                return x  # Halted
            elif result:
                pc += 1
            else:
                pc += 2
        return x  # Reached end without halting
    def check_inequivalence(scheme1, scheme2, functions, predicates, domain_set):
        for x in domain_set:
            result1 = simulate_scheme(scheme1, functions, predicates, x)
            result2 = simulate_scheme(scheme2, functions, predicates, x)
            if result1 is not None and result2 is not None and result1 != result2:
                return True
        return False
    functions = {
        "f": lambda x: x + 1,
    }
    predicates = {
        "p": lambda x: x > 0,
    }
    domain_set = [0, 1, 2, 3]  # Example domain set, modify as needed
    scheme1 = [
        "x <--- f(x)",
        "if p(x) then goto 1 else goto 2",
        "halt"
    ]
    scheme2 = [
        "x <--- f(f(x))",
        "if p(x) then goto 2 else goto 1",
        "halt"
    ]
    result = check_inequivalence(scheme1, scheme2, functions, predicates, domain_set)
    print("The two Ianov schemes are" + (" not" if result else "") + " strongly inequivalent.")
