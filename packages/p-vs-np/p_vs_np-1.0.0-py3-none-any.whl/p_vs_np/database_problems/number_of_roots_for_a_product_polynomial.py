#number of roots for a product polynomial


    # Convert the product polynomial to a list of coefficients

    # Use numpy's roots function to calculate the roots of the polynomial

    # Count the number of distinct roots


# Example usage




if __name__ == '__main__':
    import numpy as np
    def count_roots(product_polynomial):
        coefficients = list(product_polynomial)
        roots = np.roots(coefficients)
        num_roots = len(set(roots))
        return num_roots
    polynomial = [1, -3, 2]  # Represents the polynomial (x-1)(x-2)
    num_roots = count_roots(polynomial)
    print("Number of roots:", num_roots)
