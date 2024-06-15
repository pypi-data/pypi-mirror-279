#Largest Common Subgraph


# Define the graphs to be compared

# Add edges and nodes to the graphs

# Create the set of all subgraphs of G1

# Create the set of all subgraphs of G2

# Initialize the largest common subgraph

# Find the largest common subgraph

# Print the largest common subgraph

if __name__ == '__main__':
    import itertools
    G1 = nx.Graph()
    G2 = nx.Graph()
    G1.add_edges_from([(1,2), (2,3), (3,4)])
    G2.add_edges_from([(5,6), (6,7), (7,8)])
    subgraphs_G1 = [G1.subgraph(c).copy() for c in itertools.combinations(G1.nodes(), 2)]
    subgraphs_G2 = [G2.subgraph(c).copy() for c in itertools.combinations(G2.nodes(), 2)]
    LCS = nx.Graph()
    for subgraph1 in subgraphs_G1:
        for subgraph2 in subgraphs_G2:
            if nx.is_isomorphic(subgraph1, subgraph2) and len(subgraph1.nodes()) > len(LCS.nodes()):
                LCS = subgraph1.copy()
    print(LCS.edges())
