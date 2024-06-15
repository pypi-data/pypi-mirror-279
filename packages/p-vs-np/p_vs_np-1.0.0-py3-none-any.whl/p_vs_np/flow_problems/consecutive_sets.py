#Consecutive Sets








# Example usage



if __name__ == '__main__':
    def consecutive_sets(set_elements, subsets, K):
        n = len(set_elements)
        result = []
        def backtrack(start, selected):
            if len(selected) >= K:
                result.extend(selected)
                return True
            if start == n:
                return False
            for i in range(start, n):
                subset = subsets[i]
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
    set_elements = [1, 2, 3, 4, 5, 6]
    subsets = [
        {1, 2, 3},
        {4, 5, 6},
        {2, 4},
        {1, 3, 6}
    ]
    K = 2
    result = consecutive_sets(set_elements, subsets, K)
    if result:
        print("Selected subsets:", result)
    else:
        print("No valid selection found.")
