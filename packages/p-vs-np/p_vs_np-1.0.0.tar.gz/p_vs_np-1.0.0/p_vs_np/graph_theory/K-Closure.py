#K-Closure


# Define the graph

# Add edges and nodes to the graph

# Define the value of k

# Initialize the k-closure

# Check for k-closure

# Print the result

if __name__ == '__main__':
    import itertools
    G = nx.Graph()
    G.add_edges_from([(1,2), (2,3), (3,4)])
    k = 2
    k_closure = nx.Graph()
    for vertex in G.nodes():
        for neighbor in nx.single_source_shortest_path_length(G, vertex, k).keys():
            k_closure.add_edge(vertex, neighbor)
    print("The k-closure of the graph is: ", k_closure.edges())
