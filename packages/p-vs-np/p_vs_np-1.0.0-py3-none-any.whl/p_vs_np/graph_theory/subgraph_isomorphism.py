#Subgraph Isomorphism


# Define the graphs to be compared

# Add edges and nodes to the graphs

# Create a GraphMatcher object

# Check for subgraph isomorphism

if __name__ == '__main__':
    from networkx.algorithms.isomorphism import GraphMatcher
    G1 = nx.Graph()
    G2 = nx.Graph()
    G1.add_edges_from([(1,2), (2,3), (3,4)])
    G2.add_edges_from([(5,6), (6,7), (7,8)])
    gm = GraphMatcher(G1, G2)
    if gm.subgraph_is_isomorphic():
        print("The graphs are subgraph isomorphic.")
    else:
        print("The graphs are not subgraph isomorphic.")
