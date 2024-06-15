#Left-Right hackenbush for redwood furniture

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
    # Check if the current position is winning for the current player
    if graph.is_empty():
        # No edges left, current player wins
        return True

    # Check if there is a move that leads to a losing position for the opponent
    for edge in graph.edges:
        u, v = edge
        # Try removing the edge and check if the resulting position is losing for the opponent
        graph.remove_edge(u, v)
        if not is_winnable(graph):
            # Found a winning move for the current player
            graph.add_edge(u, v)  # Restore the removed edge
            return True
        graph.add_edge(u, v)  # Restore the removed edge

    # No winning move found, current player loses
    return False

def play_game():
    # Create the initial graph representing the redwood furniture pieces
    graph = Graph()
    # Add edges to the graph

    # Main game loop
    current_player = 1
    while True:
        # Print the current state of the graph
        graph.print_graph()

        # Prompt the current player for their move
        print("Player", current_player, "turn:")
        u = int(input("Enter the starting vertex of the edge to remove: "))
        v = int(input("Enter the ending vertex of the edge to remove: "))

        # Remove the chosen edge from the graph
        graph.remove_edge(u, v)

        # Check if the current player wins
        if is_winnable(graph):
            print("Player", current_player, "wins!")
            break

        # Switch to the next player
        current_player = 2 if current_player == 1 else 1

# Run the game
play_game()
