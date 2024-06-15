#Rooted Tree Storage Assignment




# Example usage



if __name__ == '__main__':
    def rooted_tree_storage_assignment(X, C, K):
        n = len(X)
        m = len(C)
        dp = [[float('inf')] * (m + 1) for _ in range(n + 1)]
        dp[0][0] = 0
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                cost = abs(len(X[i - 1]) - len(C[j - 1]))
                dp[i][j] = min(dp[i][j - 1], dp[i - 1][j - 1] + cost)
        if dp[n][m] <= K:
            return True
        else:
            return False
    X = [[1, 2], [2, 3, 4], [4, 5]]
    C = [[1], [2, 3], [4, 5]]
    K = 3
    result = rooted_tree_storage_assignment(X, C, K)
    if result:
        print("A valid collection C' exists.")
    else:
        print("No valid collection C' exists.")
