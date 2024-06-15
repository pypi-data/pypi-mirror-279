#Unconnected Subgraph






if __name__ == '__main__':
    from itertools import combinations
    def unconnected_subgraph(graph):
        max_subgraph = nx.Graph()
        for vertex in graph:
            for subset in combinations(graph.nodes(), vertex):
                subgraph = graph.subgraph(subset)
                if not nx.is_connected(subgraph):
                    if len(subset) > len(max_subgraph):
                        max_subgraph = subgraph
        return max_subgraph
    graph = nx.Graph()
    graph.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)])
    subgraph = unconnected_subgraph(graph)
    print(subgraph.edges())
