#Generalized Hex (*)


# Create a hexagonal grid

# Function to check if a move is valid

# Function to check if a player has won
    # Check if there is a path from top to bottom for the given player




# Function to print the current state of the board

# Game loop






if __name__ == '__main__':
    import numpy as np
    size = 6  # Size of the hexagonal grid
    board = np.zeros((size, size), dtype=int)
    def is_valid_move(row, col):
        return 0 <= row < size and 0 <= col < size and board[row, col] == 0
    def is_winner(player):
        visited = set()
        def dfs(row, col):
            if row < 0 or row >= size or col < 0 or col >= size or board[row, col] != player or (row, col) in visited:
                return False
            if row == size - 1:
                return True
            visited.add((row, col))
            return any(
                dfs(row + dr, col + dc)
                for dr, dc in [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
            )
        return any(dfs(0, col) for col in range(size))
    def print_board():
        symbols = [" ", "X", "O"]
        for row in range(size):
            print(" " * row, end="")
            for col in range(size):
                print(symbols[board[row, col]], end=" ")
            print()
    current_player = 1  # Player 1 starts
    while True:
        print_board()
        row = int(input("Enter the row: "))
        col = int(input("Enter the column: "))
        if not is_valid_move(row, col):
            print("Invalid move. Try again.")
            continue
        board[row, col] = current_player
        if is_winner(current_player):
            print(f"Player {current_player} wins!")
            break
        current_player = 3 - current_player  # Switch players
    print_board()
