#Square-Tiling

    # Check if the grid can be tiled with dominos

    # Base case: all cells are covered

    # Find the first empty cell
                # Check horizontal placement

                # Check vertical placement



# Example usage



if __name__ == '__main__':
    def can_tile(grid):
        if all(all(cell == 1 for cell in row) for row in grid):
            return True
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 0:
                    if i < len(grid) - 1 and grid[i + 1][j] == 0:
                        grid[i][j] = grid[i + 1][j] = 1  # Place horizontal domino
                        if can_tile(grid):  # Recurse on the modified grid
                            return True
                        grid[i][j] = grid[i + 1][j] = 0  # Reset grid
                    if j < len(grid[0]) - 1 and grid[i][j + 1] == 0:
                        grid[i][j] = grid[i][j + 1] = 1  # Place vertical domino
                        if can_tile(grid):  # Recurse on the modified grid
                            return True
                        grid[i][j] = grid[i][j + 1] = 0  # Reset grid
                    return False  # No valid placement found
        return True  # All cells are already covered
    grid = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    if can_tile(grid):
        print("The grid can be tiled.")
    else:
        print("The grid cannot be tiled.")
