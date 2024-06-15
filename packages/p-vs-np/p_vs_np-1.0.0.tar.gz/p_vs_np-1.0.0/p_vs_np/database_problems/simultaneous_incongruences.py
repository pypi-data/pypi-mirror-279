#Simultaneous Incongruences



    # Create symbols for unknown variables

    # Create a list of equations using the symbols

    # Solve the simultaneous equations

    # Check if a solution exists


# Example usage



if __name__ == '__main__':
    from sympy import symbols, Eq, solve
    def is_simultaneous_solution(equations):
        variables = symbols('x:%d' % len(equations))
        eqs = [Eq(var, a, modulus=m) for var, a, m in equations]
        solution = solve(eqs, variables)
        return bool(solution)
    equations = [(symbols('x1'), 1, 3),
                 (symbols('x2'), 2, 4),
                 (symbols('x3'), 2, 5)]
    has_solution = is_simultaneous_solution(equations)
    print("A simultaneous solution exists:", has_solution)
