#First Order Theory of Equality






















# Example usage



if __name__ == '__main__':
    import itertools
    class Variable:
        def __init__(self, name):
            self.name = name
        def __repr__(self):
            return self.name
    class Function:
        def __init__(self, name, arguments):
            self.name = name
            self.arguments = arguments
        def __repr__(self):
            return f"{self.name}({', '.join(str(arg) for arg in self.arguments)})"
    class Predicate:
        def __init__(self, name, arguments):
            self.name = name
            self.arguments = arguments
        def __repr__(self):
            return f"{self.name}({', '.join(str(arg) for arg in self.arguments)})"
    def is_formula_satisfiable(formula, constants, variables, functions, predicates):
        for assignment in itertools.product(constants, repeat=len(variables)):
            assignment_dict = dict(zip(variables, assignment))
            if evaluate_formula(formula, assignment_dict, functions, predicates):
                return True
        return False
    def evaluate_formula(formula, assignment, functions, predicates):
        if isinstance(formula, Variable):
            return assignment[formula]
        if isinstance(formula, Function):
            evaluated_arguments = [evaluate_formula(arg, assignment, functions, predicates) for arg in formula.arguments]
            return Function(formula.name, evaluated_arguments)
        if isinstance(formula, Predicate):
            evaluated_arguments = [evaluate_formula(arg, assignment, functions, predicates) for arg in formula.arguments]
            return Predicate(formula.name, evaluated_arguments)
        if formula[0] == "=":
            term1 = evaluate_formula(formula[1], assignment, functions, predicates)
            term2 = evaluate_formula(formula[2], assignment, functions, predicates)
            return term1 == term2
        if formula[0] == "∀":
            variable = formula[1]
            subformula = formula[2]
            return all(evaluate_formula(subformula, {**assignment, variable: constant}, functions, predicates)
                       for constant in constants)
        if formula[0] == "∃":
            variable = formula[1]
            subformula = formula[2]
            return any(evaluate_formula(subformula, {**assignment, variable: constant}, functions, predicates)
                       for constant in constants)
    constants = ["a", "b"]
    variables = [Variable("x"), Variable("y")]
    functions = []
    predicates = []
    formula = [
        "=",
        Function("f", [Variable("x")]),
        Function("f", [Variable("y")])
    ]
    is_satisfiable = is_formula_satisfiable(formula, constants, variables, functions, predicates)
    print("Is formula satisfiable:", is_satisfiable)
