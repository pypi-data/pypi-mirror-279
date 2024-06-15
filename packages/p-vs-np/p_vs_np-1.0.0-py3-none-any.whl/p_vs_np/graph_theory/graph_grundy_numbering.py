##Graph Grundy Numbering


# Define the graph

# Add edges and nodes to the graph

# Define the maximum number of colors

# Initialize the grundy numbers

# Define the backtracking function
        # Assign the smallest available grundy number

# Assign the grundy numbers

# Print the result

if __name__ == '__main__':
    from collections import defaultdict
    G = nx.Graph()
    G.add_edges_from([(1,2), (2,3), (3,4)])
    max_colors = 3
    grundy = defaultdict(int)
    def backtrack(v, c):
        if v not in grundy:
            used_colors = set()
            for neighbor in G[v]:
                if neighbor in grundy:
                    used_colors.add(grundy[neighbor])
            for color in range(max_colors):
                if color not in used_colors:
                    grundy[v] = color
                    break
        return grundy[v]
    for v in G.nodes():
        backtrack(v, max_colors)
    print("Grundy Numbers:", grundy)
