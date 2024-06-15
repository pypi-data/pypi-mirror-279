#Oriented Diameter


# Define the directed graph

# Add edges and nodes to the graph

# Initialize the distance matrix

# Use the Floyd-Warshall algorithm to find the oriented diameter

# Find the maximum length of any simple path

# Print the result

if __name__ == '__main__':
    import numpy as np
    G = nx.DiGraph()
    G.add_edges_from([(1,2), (2,3), (3,4)])
    n = len(G.nodes())
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            try:
                dist[i][j] = nx.shortest_path_length(G, i, j)
            except nx.NetworkXNoPath:
                dist[i][j] = float('inf')
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    oriented_diameter = max(dist.max(axis=0))
    print("The oriented diameter of the graph is: ", oriented_diameter)
