#Minimum Equivalent Digraph






if __name__ == '__main__':
    from itertools import permutations
    def min_equivalent_digraph(graph):
        min_digraph = nx.DiGraph()
        for edges in permutations(graph.edges()):
            digraph = nx.DiGraph()
            digraph.add_edges_from(edges)
            if digraph.number_of_edges() == graph.number_of_edges():
                if len(digraph.nodes()) < len(min_digraph.nodes()):
                    min_digraph = digraph
        return min_digraph
    graph = nx.Graph()
    graph.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)])
    digraph = min_equivalent_digraph(graph)
    print(digraph.edges())
