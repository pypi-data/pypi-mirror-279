#Prime Attribution Name







# Example usage


if __name__ == '__main__':
    def is_prime_attribute(X, A, F):
        for key in powerset(A):
            if X in key and is_key(key, A, F):
                return True
        return False
    def is_key(attributes, A, F):
        closure = set(attributes)
        updated = True
        while updated:
            updated = False
            for B, C in F:
                if B.issubset(closure) and not C.issubset(closure):
                    closure.update(C)
                    updated = True
        return closure == set(A)
    def powerset(s):
        powerset = [[]]
        for elem in s:
            powerset.extend([subset + [elem] for subset in powerset])
        return powerset
    A = ['A', 'B', 'C', 'D']
    F = [({'A'}, {'B', 'C'}), ({'B'}, {'D'})]
    X = 'C'
    result = is_prime_attribute(X, A, F)
    if result:
        print(f"{X} is a prime attribute.")
    else:
        print(f"{X} is not a prime attribute.")
