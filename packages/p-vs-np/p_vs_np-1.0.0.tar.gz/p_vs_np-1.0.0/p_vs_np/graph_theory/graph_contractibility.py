#Graph Contractibility


# Define the graph

# Add edges and nodes to the graph

# Define the number of steps

# Create the set of all subgraphs of G

# Initialize the step count

# Check if the graph can be contracted to a single node in k steps

# Print the result


if __name__ == '__main__':
    import itertools
    G = nx.Graph()
    G.add_edges_from([(1,2), (2,3), (3,4)])
    k = 2
    subgraphs = [G.subgraph(c).copy() for c in itertools.combinations(G.nodes(), 2)]
    step_count = 0
    while len(G.nodes()) > 1:
        step_count += 1
        if step_count > k:
            print("The graph cannot be contracted to a single node in {} steps.".format(k))
            break
        edge = G.edges()[0]
        G.remove_nodes_from(edge)
        G = nx.contracted_nodes(G, edge[0], edge[1])
    if step_count <= k:
        print("The graph can be contracted to a single node in {} steps.".format(step_count))
