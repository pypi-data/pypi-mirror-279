#Minimum Cardinality Key

    # Generate all subsets of A with cardinality <= M

    # Check if each subset is a key





# Example usage


if __name__ == '__main__':
    def is_minimum_cardinality_key(A, F, M):
        subsets = [[]]
        for a in A:
            subsets.extend([subset + [a] for subset in subsets])
        subsets = [subset for subset in subsets if len(subset) <= M]
        for subset in subsets:
            if is_superkey(subset, A, F):
                return True
        return False
    def is_superkey(subset, A, F):
        closure = set(subset)
        updated = True
        while updated:
            updated = False
            for B, C in F:
                if B.issubset(closure) and not C.issubset(closure):
                    closure.update(C)
                    updated = True
        return closure == set(A)
    A = ['A', 'B', 'C']
    F = [({'A'}, {'B'}), ({'B'}, {'C'})]
    M = 2
    result = is_minimum_cardinality_key(A, F, M)
    if result:
        print("There exists a minimum cardinality key.")
    else:
        print("No minimum cardinality key exists.")
