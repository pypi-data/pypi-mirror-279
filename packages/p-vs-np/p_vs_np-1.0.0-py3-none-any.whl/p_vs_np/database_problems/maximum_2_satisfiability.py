#Maximum 2-Satisfiability













# Example usage



if __name__ == '__main__':
    def maximize_2sat(clauses):
        variables = set()
        for clause in clauses:
            variables.update(map(abs, clause))
        assignment = {}
        for var in variables:
            assignment[var] = True  # Initial assignment
        while True:
            satisfied_clauses = count_satisfied_clauses(clauses, assignment)
            improved = False
            for var in variables:
                assignment[var] = not assignment[var]  # Flip the assignment
                new_satisfied_clauses = count_satisfied_clauses(clauses, assignment)
                if new_satisfied_clauses > satisfied_clauses:
                    satisfied_clauses = new_satisfied_clauses
                    improved = True
                else:
                    assignment[var] = not assignment[var]  # Flip back
            if not improved:
                break
        return assignment, satisfied_clauses
    def count_satisfied_clauses(clauses, assignment):
        count = 0
        for clause in clauses:
            if any((literal > 0 and assignment[literal]) or (literal < 0 and not assignment[-literal]) for literal in clause):
                count += 1
        return count
    clauses = [
        [1, 2],
        [-1, -2],
        [1, -2],
        [-1, 2]
    ]
    assignment, num_satisfied = maximize_2sat(clauses)
    print("Max 2SAT assignment:", assignment)
    print("Number of satisfied clauses:", num_satisfied)
