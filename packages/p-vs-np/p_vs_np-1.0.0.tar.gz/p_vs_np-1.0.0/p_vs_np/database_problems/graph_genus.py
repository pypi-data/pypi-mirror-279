#Graph Genus


    # Generate all possible subsets of edges of size K or less

    # Check if any edge subset forms a valid embedding


    # Create a copy of the original graph

    # Remove the edges in the subset from the copy

    # Check if the resulting graph is planar

# Example usage
    # Example instance

    # Solve the "Graph Genus" problem

    # Print the result


if __name__ == '__main__':
    import networkx as nx
    from itertools import combinations
    def graph_genus(G, K):
        edge_subsets = []
        for k in range(K + 1):
            edge_subsets.extend(combinations(G.edges(), k))
        for subset in edge_subsets:
            if is_valid_embedding(G, subset):
                return True
        return False
    def is_valid_embedding(G, edge_subset):
        embedded_graph = G.copy()
        embedded_graph.remove_edges_from(edge_subset)
        return nx.check_planarity(embedded_graph)[0]
    if __name__ == '__main__':
        G = nx.Graph()
        G.add_edges_from([(1, 2), (2, 3), (3, 1), (3, 4), (4, 1)])
        K = 1
        result = graph_genus(G, K)
        if result:
            print("Graph can be embedded on a surface of genus", K)
        else:
            print("Graph cannot be embedded on a surface of genus", K)
