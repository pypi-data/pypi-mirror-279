#Non-Divisibility of a product polynomial



# Example usage



if __name__ == '__main__':
    def is_non_divisible_polynomial(polynomial, primes):
        for prime in primes:
            if is_divisible(polynomial, prime):
                return False
        return True
    def is_divisible(polynomial, prime):
        for coefficient in polynomial:
            if coefficient % prime == 0:
                return True
        return False
    polynomial = [1, -2, 1]  # x^2 - 2x + 1
    primes = [2, 3, 5]
    is_non_divisible = is_non_divisible_polynomial(polynomial, primes)
    print("Polynomial is non-divisible by primes:", is_non_divisible)
