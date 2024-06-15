#NxN GO


# Create an empty GO board

# Function to print the current state of the GO board

# Function to check if a move is valid

# Function to make a move

# Function to check if a group of stones is surrounded

# Main game loop

if __name__ == '__main__':
    N = 9  # Size of the GO board
    board = [[' ' for _ in range(N)] for _ in range(N)]
    def print_board():
        print('  ' + ' '.join([chr(ord('A') + i) for i in range(N)]))
        for i in range(N):
            print(str(i + 1).rjust(2) + ' ' + ' '.join(board[i]))
    def is_valid_move(row, col):
        if row < 0 or row >= N or col < 0 or col >= N:
            return False
        if board[row][col] != ' ':
            return False
        return True
    def make_move(row, col, player):
        board[row][col] = player
    def is_surrounded(row, col, player):
        if row < 0 or row >= N or col < 0 or col >= N or board[row][col] != player:
            return False
        visited = set()
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))
            if r == 0 or r == N - 1 or c == 0 or c == N - 1:
                return False
            if r > 0 and board[r - 1][c] == ' ':
                return False
            if r < N - 1 and board[r + 1][c] == ' ':
                return False
            if c > 0 and board[r][c - 1] == ' ':
                return False
            if c < N - 1 and board[r][c + 1] == ' ':
                return False
            if r > 0 and board[r - 1][c] == player:
                stack.append((r - 1, c))
            if r < N - 1 and board[r + 1][c] == player:
                stack.append((r + 1, c))
            if c > 0 and board[r][c - 1] == player:
                stack.append((r, c - 1))
            if c < N - 1 and board[r][c + 1] == player:
                stack.append((r, c + 1))
        return True
    current_player = 'X'
    while True:
        print_board()
        print("Player", current_player + "'s turn")
        move = input("Enter your move (e.g., A3): ").strip().upper()
        if move == 'QUIT':
            break
        col = ord(move[0]) - ord('A')
        row = int(move[1:]) - 1
        if not is_valid_move(row, col):
            print("Invalid move! Try again.")
            continue
        make_move(row, col, current_player)
        if is_surrounded(row, col, current_player):
            print_board()
            print("Player", current_player, "wins!")
            break
        current_player = 'O' if current_player == 'X' else 'X'
