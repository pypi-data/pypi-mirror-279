#Kernel


# Define the graph

# Add edges and nodes to the graph

# Create the set of all subgraphs of G

# Initialize the kernel

# Check for kernel

# Print the result

if __name__ == '__main__':
    import itertools
    G = nx.Graph()
    G.add_edges_from([(1,2), (2,3), (3,4)])
    subgraphs = [G.subgraph(c).copy() for c in itertools.combinations(G.nodes(), 2)]
    kernel = None
    for subgraph in subgraphs:
        is_kernel = True
        for vertex in G.nodes():
            if vertex not in subgraph.nodes():
                if not any(neighbor in subgraph.nodes() for neighbor in G.neighbors(vertex)):
                    is_kernel = False
                    break
        if is_kernel:
            kernel = subgraph
            break
    if kernel:
        print("The graph has a kernel:", kernel.nodes())
    else:
        print("The graph has no kernel.")
