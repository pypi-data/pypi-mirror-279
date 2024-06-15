#Longest Common Subsequence


    # Create a table to store the lengths of the longest common subsequences

    # Fill the table using dynamic programming

    # Reconstruct the longest common subsequence



# Example usage



if __name__ == '__main__':
    def longest_common_subsequence(seq1, seq2):
        m = len(seq1)
        n = len(seq2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0 or j == 0:
                    dp[i][j] = 0
                elif seq1[i - 1] == seq2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        subsequence = ""
        i, j = m, n
        while i > 0 and j > 0:
            if seq1[i - 1] == seq2[j - 1]:
                subsequence = seq1[i - 1] + subsequence
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                i -= 1
            else:
                j -= 1
        return subsequence
    seq1 = "ABCDGH"
    seq2 = "AEDFHR"
    result = longest_common_subsequence(seq1, seq2)
    print("Longest Common Subsequence:", result)
