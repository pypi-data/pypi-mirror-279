#Simultaneous Divisibility of Linear Polynomials(*)


    # Separate the equations into expressions and moduli

    # Reduce equations to the form x ≡ b (mod m)

    # Use Chinese Remainder Theorem to find a common solution

# Example usage


if __name__ == '__main__':
    from sympy import symbols, Eq, solve
    from sympy.ntheory.modular import crt
    def is_simultaneous_solution(equations):
        x = symbols('x')
        exprs = []
        moduli = []
        for eq in equations:
            f_x, m = eq
            exprs.append(eval(f_x))
            moduli.append(m)
        residues = []
        for expr, m in zip(exprs, moduli):
            solutions = solve(Eq(expr, 0), x)
            if solutions:
                residues.append(solutions[0] % m)
            else:
                return False  # No solution found for this congruence
        try:
            solution = crt(moduli, residues)
            return solution is not None
        except ValueError:
            return False
    equations = [('2*x + 1', 3),
                 ('3*x - 1', 4),
                 ('x + 2', 5)]
    has_solution = is_simultaneous_solution(equations)
    print("A simultaneous solution exists:", has_solution)
