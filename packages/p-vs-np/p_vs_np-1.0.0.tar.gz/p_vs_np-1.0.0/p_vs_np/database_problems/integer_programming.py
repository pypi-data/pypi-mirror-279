#Integer Programming



    # Create the LP problem

    # Decision variables

    # Objective function

    # Constraints

    # Solve the problem

    # Print the solution


# Example usage


if __name__ == '__main__':
    from pulp import LpProblem, LpVariable, LpInteger, LpMaximize, LpStatus, lpSum
    def solve_integer_programming():
        problem = LpProblem("Integer Programming", LpMaximize)
        x = LpVariable("x", lowBound=0, cat=LpInteger)
        y = LpVariable("y", lowBound=0, cat=LpInteger)
        problem += 3 * x + 2 * y
        problem += 2 * x + y <= 8
        problem += x + 2 * y <= 9
        problem.solve()
        if problem.status == LpStatusOptimal:
            print("Optimal solution found:")
            print("x =", x.varValue)
            print("y =", y.varValue)
            print("Objective =", problem.objective.value())
        else:
            print("No feasible solution found.")
    if __name__ == "__main__":
        solve_integer_programming()
