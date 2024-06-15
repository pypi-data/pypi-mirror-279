#Chromatic Index



    # Check if the chromatic index is K or less


# Example usage
    # Example instance

    # Solve the "Chromatic Index" problem

    # Print the result


if __name__ == '__main__':
    import networkx as nx
    def chromatic_index(G, K):
        max_degree = max(dict(G.degree()).values())
        if max_degree <= K:
            return True
        return False
    if __name__ == '__main__':
        G = nx.Graph()
        G.add_edges_from([(1, 2), (2, 3), (3, 1)])
        K = 2
        result = chromatic_index(G, K)
        if result:
            print("Graph has chromatic index", K, "or less")
        else:
            print("Graph does not have chromatic index", K, "or less")
