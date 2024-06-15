#Metric Dimension


# Define the graph

# Add edges and nodes to the graph

# Create all possible subsets

# Check for metric dimension

if __name__ == '__main__':
    import itertools
    G = nx.Graph()
    G.add_edges_from([(1,2), (2,3), (3,4)])
    possible_subsets = [set(c) for c in itertools.combinations(G.nodes(), 2)]
    for subset in possible_subsets:
        is_resolving = True
        for v, u in itertools.combinations(G.nodes(), 2):
            v_distances = {n: nx.shortest_path_length(G, v, n) for n in subset}
            u_distances = {n: nx.shortest_path_length(G, u, n) for n in subset}
            if v_distances == u_distances:
                is_resolving = False
                break
        if is_resolving:
            print("The subset", subset, "is a resolving set")
            break
    else:
        print("The graph does not have a resolving set.")
