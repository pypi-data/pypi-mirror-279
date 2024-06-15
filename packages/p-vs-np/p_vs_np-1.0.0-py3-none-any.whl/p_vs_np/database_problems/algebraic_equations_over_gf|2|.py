#Algebraic equations over GF|2|

import numpy as np

def solve_algebraic_equations(coefficients, constants):
    # Convert the coefficients and constants to a numpy array
    A = np.array(coefficients)
    b = np.array(constants)

    # Solve the system of equations using Gaussian elimination
    augmented_matrix = np.column_stack((A, b))
    rref, _ = np.linalg.qr(augmented_matrix)

    # Check if the system has a solution
    rank_A = np.linalg.matrix_rank(A)
    rank_augmented = np.linalg.matrix_rank(augmented_matrix)

    if rank_A == rank_augmented:
        return True  # System has a solution
    else:
        return False  # System does not have a solution

# Example usage
coefficients = [[1, 0, 1], [0, 1, 1], [1, 1, 0]]
constants = [1, 0, 1]

has_solution = solve_algebraic_equations(coefficients, constants)
print("Has solution:", has_solution)

