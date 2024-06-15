#Quadratic Assignment Problem



# Example usage:



# Print the solution

if __name__ == '__main__':
    from pyqap import QAPSolver
    def solve_quadratic_assignment_problem(distances, flows):
        solver = QAPSolver(distances, flows)
        solution = solver.solve()
        return solution
    distances = [
        [0, 1, 2],
        [1, 0, 3],
        [2, 3, 0]
    ]
    flows = [
        [0, 5, 8],
        [5, 0, 2],
        [8, 2, 0]
    ]
    solution = solve_quadratic_assignment_problem(distances, flows)
    print("Optimal permutation:", solution.permutation)
    print("Objective function value:", solution.value)
