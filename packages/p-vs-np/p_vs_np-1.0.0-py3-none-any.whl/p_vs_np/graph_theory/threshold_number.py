
# Define the graph

# Add edges and nodes to the graph

# Initialize the threshold number

# Check for threshold number

# Print the result

if __name__ == '__main__':
    import networkx as nx
    import itertools
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 4)])
    threshold_number = None
    for i in range(1, len(G.nodes())):
        for removed_nodes in itertools.combinations(G.nodes(), i):
            H = G.copy()
            H.remove_nodes_from(removed_nodes)
            if not nx.is_connected(H):
                threshold_number = i
                break
        if threshold_number:
            break
    if threshold_number:
        print("The threshold number of the graph is:", threshold_number)
    else:
        print("The graph is already disconnected.")
