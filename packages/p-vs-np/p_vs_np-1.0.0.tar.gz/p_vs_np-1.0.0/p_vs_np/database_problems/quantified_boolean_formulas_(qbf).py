#Quantified Boolean Formulas (QBF)












# Example usage



if __name__ == '__main__':
    def evaluate_formula(formula, variables, assignment):
        for quantifier, var in formula[0]:
            if quantifier == 'FORALL':
                variables[var] = assignment[var]
            else:  # quantifier is 'EXISTS'
                variables[var] = not assignment[var]
        return evaluate_expression(formula[1], variables)
    def evaluate_expression(expression, variables):
        if isinstance(expression, bool):
            return expression
        if expression[0] == 'AND':
            return all(evaluate_expression(subexpr, variables) for subexpr in expression[1:])
        elif expression[0] == 'OR':
            return any(evaluate_expression(subexpr, variables) for subexpr in expression[1:])
        elif expression[0] == 'NOT':
            return not evaluate_expression(expression[1], variables)
    def is_qbf_satisfiable(formula, num_variables):
        variables = [False] * num_variables
        for assignment in product([False, True], repeat=num_variables):
            assignment_dict = {i: assignment[i] for i in range(num_variables)}
            if evaluate_formula(formula, variables, assignment_dict):
                return True
        return False
    formula = [
        [('FORALL', 0), ('EXISTS', 1)],
        ['AND', ['OR', 'x0', 'x1'], ['OR', ['NOT', 'x0'], ['NOT', 'x1']]]
    ]
    num_variables = 2
    is_satisfiable = is_qbf_satisfiable(formula, num_variables)
    print("Is QBF satisfiable:", is_satisfiable)
