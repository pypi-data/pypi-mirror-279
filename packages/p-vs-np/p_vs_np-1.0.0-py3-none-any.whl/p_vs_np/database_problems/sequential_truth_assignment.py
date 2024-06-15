#Sequential Truth Assignment


    # Convert the formula to CNF format expected by pycosat

    # Solve the CNF formula using pycosat

    # Check if the solution is satisfiable

# Example usage




if __name__ == '__main__':
    import pycosat
    def is_satisfiable(formula):
        cnf_formula = [list(clause) for clause in formula]
        solution = pycosat.solve(cnf_formula)
        return solution != "UNSAT"
    formula = [[1, -2, 3], [-1, 2, 3], [1, 2, -3]]  # CNF formula
    is_satisfiable = is_satisfiable(formula)
    if is_satisfiable:
        print("The formula has a satisfying sequential truth assignment.")
    else:
        print("The formula does not have a satisfying sequential truth assignment.")
