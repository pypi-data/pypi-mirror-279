#Truth Functionally Complete Connectives
















# Example usage


if __name__ == '__main__':
    def evaluate_expression(expression, assignment):
        stack = []
        for token in expression:
            if token in ['AND', 'OR', 'NOT']:
                if token == 'AND':
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                    result = operand1 and operand2
                elif token == 'OR':
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                    result = operand1 or operand2
                else:  # token is 'NOT'
                    operand = stack.pop()
                    result = not operand
                stack.append(result)
            else:
                variable = token[1:]
                if token[0] == '-':
                    value = not assignment[variable]
                else:
                    value = assignment[variable]
                stack.append(value)
        return stack.pop()
    def is_truth_functionally_complete(connectives, variables):
        truth_values = [False, True]
        truth_functions = []
        for assignment in product(truth_values, repeat=len(variables)):
            assignment_dict = {variables[i]: assignment[i] for i in range(len(variables))}
            truth_function = []
            for truth_value in truth_values:
                expression = ['OR']
                for var in variables:
                    expression.append(['AND', var, truth_value])
                expression.append(['AND', '-'+connectives[0], '-'+connectives[0]])
                for i in range(1, len(connectives)):
                    expression = ['OR', expression, ['AND', '-'+connectives[i], '-'+connectives[i]]]
                result = evaluate_expression(expression, assignment_dict)
                truth_function.append(result)
            truth_functions.append(truth_function)
        return len(set(truth_functions)) == 2 ** (2 ** len(variables))
    connectives = ['AND', 'OR', 'NOT']
    variables = ['x', 'y']
    is_complete = is_truth_functionally_complete(connectives, variables)
    print("Is truth functionally complete:", is_complete)
