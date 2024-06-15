#Graph Isomorphism



# Example usage
    # Example graphs


    # Check if the graphs are isomorphic

if __name__ == '__main__':
    import networkx as nx
    def is_graph_isomorphic(graph1, graph2):
        return nx.is_isomorphic(graph1, graph2)
    if __name__ == '__main__':
        graph1 = nx.Graph()
        graph1.add_edges_from([(1, 2), (2, 3), (3, 1)])
        graph2 = nx.Graph()
        graph2.add_edges_from([(4, 5), (5, 6), (6, 4)])
        if is_graph_isomorphic(graph1, graph2):
            print("The graphs are isomorphic.")
        else:
            print("The graphs are not isomorphic.")
