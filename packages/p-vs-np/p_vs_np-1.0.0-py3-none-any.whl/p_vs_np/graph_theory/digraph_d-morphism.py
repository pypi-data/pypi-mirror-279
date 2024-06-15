#Digraph D-Morphism


# Define the directed graphs

# Add edges and nodes to the graphs

# Create a DiGraphMatcher object

# Check for digraph d-morphism

if __name__ == '__main__':
    from networkx.algorithms.isomorphism import DiGraphMatcher
    G = nx.DiGraph()
    H = nx.DiGraph()
    G.add_edges_from([(1,2), (2,3), (3,4)])
    H.add_edges_from([(5,6), (6,7), (7,8)])
    gm = DiGraphMatcher(G, H)
    if gm.subgraph_is_isomorphic():
        print("There exists a d-morphism from G to H.")
    else:
        print("There is no d-morphism from G to H.")
