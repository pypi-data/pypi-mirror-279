#2-dimensional Consecutive Sets








# Example usage



if __name__ == '__main__':
    def consecutive_sets_2d(grid, subsets, K):
        rows = len(grid)
        cols = len(grid[0])
        result = []
        def backtrack(start, selected):
            if len(selected) >= K:
                result.extend(selected)
                return True
            if start == rows:
                return False
            for i in range(start, rows):
                for j in range(cols):
                    subset = subsets[grid[i][j]]
                    if is_valid(subset, selected):
                        if backtrack(i + 1, selected + [subset]):
                            return True
        def is_valid(subset, selected):
            for element in subset:
                for s in selected:
                    if element in s:
                        return False
            return True
        if backtrack(0, []):
            return result
        return None
    grid = [
        [0, 0, 1, 1],
        [1, 2, 2, 3],
        [1, 2, 4, 4]
    ]
    subsets = [
        {1, 2},
        {3},
        {4}
    ]
    K = 2
    result = consecutive_sets_2d(grid, subsets, K)
    if result:
        print("Selected subsets:", result)
    else:
        print("No valid selection found.")
