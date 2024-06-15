#Minimizing Dummy Activities in PERT Networks


    # Calculate the indegree of each node

    # Initialize the dynamic programming table

    # Iterate through the PERT network


    # Find the minimum number of dummy activities


# Example usage:



if __name__ == '__main__':
    def minimize_dummy_activities_pert_network(adjacency_matrix):
        n = len(adjacency_matrix)  # Number of nodes in the PERT network
        indegree = [sum(adjacency_matrix[j][i] for j in range(n)) for i in range(n)]
        dp = [[float('inf')] * n for _ in range(n)]
        dp[0][0] = 0
        for i in range(n):
            for j in range(n):
                if dp[i][j] == float('inf'):
                    continue
                for k in range(n):
                    if adjacency_matrix[j][k] != 0:
                        dp[i + 1][k] = min(dp[i + 1][k], dp[i][j] + (indegree[k] - 1))
        min_dummy_activities = min(dp[-1])
        return min_dummy_activities
    adjacency_matrix = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ]
    min_dummy_activities = minimize_dummy_activities_pert_network(adjacency_matrix)
    print("Minimum number of dummy activities:", min_dummy_activities)
