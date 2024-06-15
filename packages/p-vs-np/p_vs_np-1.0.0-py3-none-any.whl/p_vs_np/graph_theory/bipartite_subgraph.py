#Bipartite Subgraph






if __name__ == '__main__':
    def bipartite_subgraph(graph):
        def is_bipartite(subgraph, graph):
            color = {}
            for vertex in subgraph:
                color[vertex] = 0
            color[subgraph[0]] = 1
            queue = [subgraph[0]]
            while queue:
                vertex = queue.pop(0)
                for neighbor in graph[vertex]:
                    if neighbor in subgraph:
                        if color[neighbor] == color[vertex]:
                            return False
                        if color[neighbor] == 0:
                            color[neighbor] = 3 - color[vertex]
                            queue.append(neighbor)
            return True
        from itertools import combinations
        max_subgraph = []
        for vertex in graph:
            for subset in combinations(graph, vertex):
                if is_bipartite(subset, graph):
                    if len(subset) > len(max_subgraph):
                        max_subgraph = subset
        return max_subgraph
    graph = {
        0: {1, 2, 3},
        1: {0, 2, 4},
        2: {0, 1, 4},
        3: {0, 4},
        4: {1, 2, 3}
    }
    subgraph = bipartite_subgraph(graph)
    print(subgraph)
