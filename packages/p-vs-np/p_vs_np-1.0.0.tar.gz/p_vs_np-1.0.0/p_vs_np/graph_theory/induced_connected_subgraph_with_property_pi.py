#Induced Connected Subgraph With Property ∏









if __name__ == '__main__':
    from itertools import combinations
    def induced_connected_subgraph_with_property(graph, property_function):
        def is_connected(subgraph, graph):
            visited = set()
            queue = [subgraph[0]]
            while queue:
                vertex = queue.pop(0)
                visited.add(vertex)
                for neighbor in graph[vertex]:
                    if neighbor not in visited and neighbor in subgraph:
                        queue.append(neighbor)
            return len(visited) == len(subgraph)
        max_subgraph = []
        for vertex in graph:
            for subset in combinations(graph, vertex):
                if is_connected(subset, graph) and property_function(subset):
                    if len(subset) > len(max_subgraph):
                        max_subgraph = subset
        return max_subgraph
    def is_clique(subgraph):
        for vertex in subgraph:
            for neighbor in subgraph:
                if vertex != neighbor and neighbor not in graph[vertex]:
                    return False
        return True
    graph = {
        0: {1, 2},
        1: {0, 2},
        2: {0, 1, 3},
        3: {2},
        4: {5, 6},
        5: {4, 6},
        6: {4, 5}
    }
    induced_subgraph = induced
    induced_connected_subgraph = induced_connected_subgraph_with_property(graph, is_clique)
    print(induced_connected_subgraph)
