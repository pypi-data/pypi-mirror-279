#Minimum Disjunctive Normal Form



























# Example usage



if __name__ == '__main__':
    from itertools import product
    def generate_minterms(expression, variables):
        minterms = []
        for assignment in product([False, True], repeat=len(variables)):
            assignment_dict = {variables[i]: assignment[i] for i in range(len(variables))}
            if evaluate_expression(expression, assignment_dict):
                minterms.append(assignment_dict)
        return minterms
    def evaluate_expression(expression, assignment):
        stack = []
        for token in expression:
            if token in ['AND', 'OR']:
                operand2 = stack.pop()
                operand1 = stack.pop()
                if token == 'AND':
                    result = operand1 and operand2
                else:
                    result = operand1 or operand2
                stack.append(result)
            else:
                variable = token[1:]
                if token[0] == '-':
                    value = not assignment[variable]
                else:
                    value = assignment[variable]
                stack.append(value)
        return stack.pop()
    def is_smaller_dnf(expression, variables, minterms):
        minterm_count = len(minterms)
        dnf_count = 0
        for assignment in product([False, True], repeat=len(variables)):
            assignment_dict = {variables[i]: assignment[i] for i in range(len(variables))}
            if evaluate_expression(expression, assignment_dict):
                dnf_count += 1
        return minterm_count <= dnf_count
    def minimize_dnf(expression, variables):
        minterms = generate_minterms(expression, variables)
        while not is_smaller_dnf(expression, variables, minterms):
            new_minterms = []
            for i in range(len(minterms)):
                for j in range(i + 1, len(minterms)):
                    minterm1 = minterms[i]
                    minterm2 = minterms[j]
                    differing_positions = []
                    for var in variables:
                        if minterm1[var] != minterm2[var]:
                            differing_positions.append(var)
                    if len(differing_positions) == 1:
                        new_minterm = dict(minterm1)
                        new_minterm[differing_positions[0]] = '-'
                        new_minterms.append(new_minterm)
            minterms.extend(new_minterms)
        return minterms
    expression = ['OR', ['AND', 'x1', 'x2'], ['AND', '-x1', 'x3'], ['AND', '-x2', '-x3']]
    variables = ['x1', 'x2', 'x3']
    minimized_dnf = minimize_dnf(expression, variables)
    print("Minimized DNF:")
    for term in minimized_dnf:
        print(term)
