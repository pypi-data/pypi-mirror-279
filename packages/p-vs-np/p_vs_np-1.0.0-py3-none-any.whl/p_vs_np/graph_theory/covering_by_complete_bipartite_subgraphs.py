#Covering By Complete Bipartite Subgraphs


        # check if the subgraph is a bipartite graph




if __name__ == '__main__':
    def covering_by_complete_bipartite_subgraphs(graph):
        def find_bipartite_subgraph(graph, vertex):
            visited = set()
            queue = [vertex]
            while queue:
                v = queue.pop(0)
                visited.add(v)
                for neighbor in graph[v]:
                    if neighbor not in visited:
                        queue.append(neighbor)
            return visited
        def is_bipartite_subgraph(graph, subgraph):
            return True
        subgraphs = []
        visited = set()
        for vertex in range(len(graph)):
            if vertex not in visited:
                subgraph = find_bipartite_subgraph(graph, vertex)
                visited = visited.union(subgraph)
                if is_bipartite_subgraph(graph, subgraph):
                    subgraphs.append(subgraph)
        return len(subgraphs)
    graph = [[0, 1, 1, 0],
             [1, 0, 1, 1],
             [1, 1, 0, 0],
             [0, 1, 0, 0]]
    print(covering_by_complete_bipartite_subgraphs(graph))
