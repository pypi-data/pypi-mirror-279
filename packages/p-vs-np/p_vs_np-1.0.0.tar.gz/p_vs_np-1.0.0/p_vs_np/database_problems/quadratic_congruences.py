#Quadratic Congruences

    # Check if a is a quadratic residue modulo n

# Example usage



if __name__ == '__main__':
    def is_quadratic_residue(a, n):
        for x in range(n):
            if (x * x) % n == a % n:
                return True
        return False
    a = 7
    n = 11
    is_residue = is_quadratic_residue(a, n)
    print(f"{a} is a quadratic residue modulo {n}: {is_residue}")
