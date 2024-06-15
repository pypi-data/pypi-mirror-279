#Consecutive Block Minimization











# Example usage



if __name__ == '__main__':
    def consecutive_block_minimization(matrix, K):
        n = len(matrix[0])
        cols = list(range(n))
        result = []
        def backtrack(start):
            if len(result) <= K:
                if start == n:
                    return True
                for i in range(start, n):
                    swap_cols(start, i)
                    if is_valid(start):
                        if backtrack(start + 1):
                            return True
                    swap_cols(start, i)
        def swap_cols(i, j):
            cols[i], cols[j] = cols[j], cols[i]
        def is_valid(start):
            nonlocal result
            blocks = 0
            for row in matrix:
                consecutive = False
                for col in cols[start:]:
                    if row[col] == 1:
                        if not consecutive:
                            blocks += 1
                            consecutive = True
                    else:
                        consecutive = False
                if blocks > K:
                    return False
            result = cols[:start]
            return True
        if backtrack(0):
            return result
        return None
    matrix = [
        [1, 0, 1, 1],
        [1, 1, 1, 0],
        [0, 1, 1, 1],
        [1, 1, 0, 0]
    ]
    K = 2
    result = consecutive_block_minimization(matrix, K)
    if result:
        print("Column permutation:", result)
    else:
        print("No valid column permutation found.")
