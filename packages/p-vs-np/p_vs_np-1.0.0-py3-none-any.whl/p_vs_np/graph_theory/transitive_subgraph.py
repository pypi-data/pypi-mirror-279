#Transitive Subgraph







if __name__ == '__main__':
    from itertools import combinations
    def transitive_subgraph(graph):
        def is_transitive(subgraph):
            for vertex1, vertex2 in subgraph.edges():
                for vertex3 in graph.successors(vertex2):
                    if vertex3 in subgraph.nodes() and (vertex1, vertex3) not in subgraph.edges():
                        return False
            return True
        max_subgraph = nx.DiGraph()
        for vertex in graph:
            for subset in combinations(graph.nodes(), vertex):
                subgraph = graph.subgraph(subset)
                if is_transitive(subgraph):
                    if len(subset) > len(max_subgraph):
                        max_subgraph = subgraph
        return max_subgraph
    graph = nx.DiGraph()
    graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])
    subgraph = transitive_subgraph(graph)
    print(subgraph.edges())
