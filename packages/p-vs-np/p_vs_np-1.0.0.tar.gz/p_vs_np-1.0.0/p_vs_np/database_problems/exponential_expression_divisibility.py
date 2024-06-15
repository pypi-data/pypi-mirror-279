#Exponential Expression Divisibility


    # Compute the prime factorization of n

    # Check if each prime factor divides the exponential expression






# Example usage


if __name__ == '__main__':
    def is_exponential_divisible(n, a, b):
        if n == 1:
            return True
        prime_factors = prime_factorization(n)
        for prime, exponent in prime_factors.items():
            if (a % prime == 0) and (b % exponent == 0):
                return True
        return False
    def prime_factorization(n):
        factors = {}
        i = 2
        while i * i <= n:
            if n % i:
                i += 1
            else:
                n //= i
                factors[i] = factors.get(i, 0) + 1
        if n > 1:
            factors[n] = factors.get(n, 0) + 1
        return factors
    n = 36
    a = 6
    b = 2
    is_divisible = is_exponential_divisible(n, a, b)
    print("Exponential expression is divisible by", n, ":", is_divisible)
