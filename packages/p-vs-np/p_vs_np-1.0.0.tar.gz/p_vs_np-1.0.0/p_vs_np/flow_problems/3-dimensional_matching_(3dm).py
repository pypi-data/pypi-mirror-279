#3-Dimensional Matching (3DM)










# Example usage:



if __name__ == '__main__':
    def find_3dm_solution(X, Y, Z):
        num_elements = len(X)
        solution = []
        def backtrack(triples):
            nonlocal solution
            if len(triples) == num_elements:
                solution = triples
                return True
            x = next(iter(X.difference(set.union(*triples))))  # Select an element from X not covered by triples
            for y in Y:
                if y in triples:
                    continue
                for z in Z:
                    if z in triples:
                        continue
                    if x in {y, z}:
                        new_triples = triples + [(x, y, z)]
                        if backtrack(new_triples):
                            return True
            return False
        if backtrack([]):
            return solution
        else:
            return []
    X = {1, 2, 3}
    Y = {4, 5, 6}
    Z = {7, 8, 9}
    solution = find_3dm_solution(X, Y, Z)
    if solution:
        print("3DM Solution:", solution)
    else:
        print("No solution found.")
