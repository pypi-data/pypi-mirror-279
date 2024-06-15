#NxN Checkers

    # Check if there is a queen in the same column

    # Check if there is a queen in the upper-left diagonal

    # Check if there is a queen in the upper-right diagonal













# Example usage



if __name__ == '__main__':
    def is_safe(board, row, col, N):
        for i in range(row):
            if board[i][col] == 1:
                return False
        i, j = row, col
        while i >= 0 and j >= 0:
            if board[i][j] == 1:
                return False
            i -= 1
            j -= 1
        i, j = row, col
        while i >= 0 and j < N:
            if board[i][j] == 1:
                return False
            i -= 1
            j += 1
        return True
    def backtrack(board, row, N):
        if row == N:
            return True
        for col in range(N):
            if is_safe(board, row, col, N):
                board[row][col] = 1
                if backtrack(board, row + 1, N):
                    return True
                board[row][col] = 0
        return False
    def solve_n_queens(N):
        board = [[0] * N for _ in range(N)]
        if backtrack(board, 0, N):
            return board
        return None
    N = 4
    solution = solve_n_queens(N)
    if solution is not None:
        print("Solution:")
        for row in solution:
            print(row)
    else:
        print("No solution found.")
