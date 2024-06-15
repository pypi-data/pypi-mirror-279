#Cyclic Ordering




# Example usage



if __name__ == '__main__':
    import itertools
    def is_valid_cyclic_ordering(graph, ordering):
        n = len(graph)
        for i in range(n):
            for j in range(i + 1, n):
                if ordering.index(graph[i]) > ordering.index(graph[j]) and not (graph[j] in graph.successors(graph[i])):
                    return False
        return True
    def solve_cyclic_ordering(graph):
        vertices = list(graph.nodes)
        permutations = itertools.permutations(vertices)
        for ordering in permutations:
            if is_valid_cyclic_ordering(graph, ordering):
                return ordering
        return None
    import networkx as nx
    graph = nx.DiGraph()
    graph.add_edges_from([(0, 1), (1, 2), (2, 0)])
    solution = solve_cyclic_ordering(graph)
    if solution is not None:
        print("Valid cyclic ordering:")
        print(solution)
    else:
        print("No valid cyclic ordering found.")
