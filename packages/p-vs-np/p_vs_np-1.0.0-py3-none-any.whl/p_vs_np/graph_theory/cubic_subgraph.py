#Cubic Subgraph






if __name__ == '__main__':
    from itertools import combinations
    def cubic_subgraph(graph):
        max_subgraph = nx.Graph()
        for vertex in graph:
            for subset in combinations(graph.nodes(), vertex):
                subgraph = graph.subgraph(subset)
                if all(d == 3 for n, d in subgraph.degree()):
                    if len(subset) > len(max_subgraph):
                        max_subgraph = subgraph
        return max_subgraph
    graph = nx.Graph()
    graph.add_edges_from([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
    subgraph = cubic_subgraph(graph)
    print(subgraph.edges())
