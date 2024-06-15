#Non-Tautology













# Example usage


if __name__ == '__main__':
    from itertools import product
    def evaluate_formula(formula, assignment):
        stack = []
        for token in formula:
            if token in ['AND', 'OR', 'IMPLIES']:
                operand2 = stack.pop()
                operand1 = stack.pop()
                if token == 'AND':
                    result = operand1 and operand2
                elif token == 'OR':
                    result = operand1 or operand2
                else:
                    result = not operand1 or operand2
                stack.append(result)
            elif token == 'NOT':
                operand = stack.pop()
                stack.append(not operand)
            else:
                variable = token[1:]
                if token[0] == '-':
                    value = not assignment[variable]
                else:
                    value = assignment[variable]
                stack.append(value)
        return stack.pop()
    def is_tautology(formula, variables):
        for assignment in product([True, False], repeat=len(variables)):
            assignment_dict = {variables[i]: assignment[i] for i in range(len(variables))}
            if not evaluate_formula(formula, assignment_dict):
                return False
        return True
    formula = ['IMPLIES', ['AND', 'x1', 'x2'], 'x1']
    variables = ['x1', 'x2']
    if is_tautology(formula, variables):
        print("Formula is a tautology")
    else:
        print("Formula is not a tautology")
