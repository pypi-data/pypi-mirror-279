#Left-Right hackenbush for redwood furniture






    # Check if the current position is winning for the current player
        # No edges left, current player wins

    # Check if there is a move that leads to a losing position for the opponent
        # Try removing the edge and check if the resulting position is losing for the opponent
            # Found a winning move for the current player

    # No winning move found, current player loses

    # Create the initial graph representing the redwood furniture pieces
    # Add edges to the graph

    # Main game loop
        # Print the current state of the graph

        # Prompt the current player for their move

        # Remove the chosen edge from the graph

        # Check if the current player wins

        # Switch to the next player

# Run the game

if __name__ == '__main__':
    class Graph:
        def __init__(self):
            self.edges = []
        def add_edge(self, u, v):
            self.edges.append((u, v))
        def remove_edge(self, u, v):
            self.edges.remove((u, v))
        def is_empty(self):
            return len(self.edges) == 0
        def print_graph(self):
            print("Graph edges:")
            for edge in self.edges:
                print(edge)
    def is_winnable(graph):
        if graph.is_empty():
            return True
        for edge in graph.edges:
            u, v = edge
            graph.remove_edge(u, v)
            if not is_winnable(graph):
                graph.add_edge(u, v)  # Restore the removed edge
                return True
            graph.add_edge(u, v)  # Restore the removed edge
        return False
    def play_game():
        graph = Graph()
        current_player = 1
        while True:
            graph.print_graph()
            print("Player", current_player, "turn:")
            u = int(input("Enter the starting vertex of the edge to remove: "))
            v = int(input("Enter the ending vertex of the edge to remove: "))
            graph.remove_edge(u, v)
            if is_winnable(graph):
                print("Player", current_player, "wins!")
                break
            current_player = 2 if current_player == 1 else 1
    play_game()
