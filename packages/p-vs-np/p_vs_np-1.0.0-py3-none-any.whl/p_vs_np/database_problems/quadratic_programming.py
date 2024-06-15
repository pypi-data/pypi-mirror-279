#Quadratic Programming



    # Define the variables

    # Define the objective function

    # Define the constraints

    # Create the problem

    # Solve the problem

    # Print the solution


# Example usage

if __name__ == '__main__':
    import cvxpy as cp
    import numpy as np
    def solve_quadratic_programming():
        x = cp.Variable(2)
        Q = np.array([[2, -1], [-1, 4]])
        c = np.array([1, -2])
        objective = cp.Minimize(cp.quad_form(x, Q) + c.T @ x)
        constraints = [x >= 0, x[0] + x[1] <= 1]
        problem = cp.Problem(objective, constraints)
        problem.solve()
        if problem.status == "optimal":
            print("Optimal solution found:")
            print("x =", x.value)
            print("Objective =", problem.value)
        else:
            print("No feasible solution found.")
    if __name__ == "__main__":
        solve_quadratic_programming()
