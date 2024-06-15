#non - containment for free B - schemes





















# Example usage



if __name__ == '__main__':
    class BScheme:
        def __init__(self, variables, tests, functions, labels):
            self.variables = variables
            self.tests = tests
            self.functions = functions
            self.labels = labels
    def is_non_contained(S1, S2):
        assignments = generate_assignments(S1.variables.union(S2.variables))
        for assignment in assignments:
            if is_non_contained_assignment(S1, S2, assignment):
                return True
        return False
    def generate_assignments(variables):
        n = len(variables)
        assignments = []
        for i in range(2 ** n):
            assignment = {}
            binary = bin(i)[2:].zfill(n)
            for j in range(n):
                assignment[variables[j]] = int(binary[j])
            assignments.append(assignment)
        return assignments
    def is_non_contained_assignment(S1, S2, assignment):
        mapping = {}
        for variable, value in assignment.items():
            mapping[variable] = value
        return not evaluate(S1, mapping) == evaluate(S2, mapping)
    def evaluate(scheme, mapping):
        for test in scheme.tests:
            label = scheme.labels[test]
            if mapping[test] != label:
                return scheme.functions[mapping[test]]
        return scheme.labels[scheme.tests[-1]]
    variables1 = {'x', 'y'}
    tests1 = {'t1', 't2'}
    functions1 = {'f1', 'f2'}
    labels1 = {'t1': 'L', 't2': 'R', 'f1': 'omega'}
    scheme1 = BScheme(variables1, tests1, functions1, labels1)
    variables2 = {'x', 'y'}
    tests2 = {'t1', 't2'}
    functions2 = {'f1', 'f2'}
    labels2 = {'t1': 'L', 't2': 'R', 'f1': 'omega'}
    scheme2 = BScheme(variables2, tests2, functions2, labels2)
    result = is_non_contained(scheme1, scheme2)
    print(result)
