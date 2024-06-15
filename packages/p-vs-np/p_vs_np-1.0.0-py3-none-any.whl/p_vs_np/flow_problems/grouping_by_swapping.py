#Grouping By Swapping














# Example usage


if __name__ == '__main__':
    def grouping_by_swapping(x, y, K):
        if len(x) != len(y):
            return False
        n = len(x)
        interchange_count = 0
        def backtrack(i):
            nonlocal interchange_count
            if i == n:
                return True
            if interchange_count > K:
                return False
            if x[i] == y[i]:
                return backtrack(i + 1)
            for j in range(i + 1, n):
                if x[j] == y[i] and x[i] == y[j]:
                    interchange_count += 1
                    x[i], x[j] = x[j], x[i]
                    if backtrack(i + 1):
                        return True
                    interchange_count -= 1
                    x[i], x[j] = x[j], x[i]
            return False
        x = list(x)
        y = list(y)
        if backtrack(0):
            return True
        return False
    x = "abacdb"
    y = "cadabd"
    K = 3
    result = grouping_by_swapping(x, y, K)
    if result:
        print("Transformation possible with at most", K, "interchanges.")
    else:
        print("Transformation not possible with at most", K, "interchanges.")
