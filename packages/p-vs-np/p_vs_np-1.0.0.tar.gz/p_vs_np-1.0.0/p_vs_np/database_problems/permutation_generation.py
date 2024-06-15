#Permutation Generation



# Example usage



if __name__ == '__main__':
    from itertools import permutations
    def generate_permutations(elements):
        return list(permutations(elements))
    elements = [1, 2, 3]
    permutations = generate_permutations(elements)
    print("Permutations:")
    for perm in permutations:
        print(perm)
