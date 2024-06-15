#Partition Into Isomorphic Subgraphs










if __name__ == '__main__':
    import networkx as nx
    def partition_into_isomorphic_subgraphs(graph):
        def is_isomorphic(subgraph1, subgraph2):
            return nx.is_isomorphic(subgraph1, subgraph2)
        def find_subgraph(graph, vertex):
            visited = set()
            subgraph = set()
            queue = [vertex]
            while queue:
                v = queue.pop(0)
                if v not in visited:
                    visited.add(v)
                    subgraph.add(v)
                    for neighbor in graph[v]:
                        if neighbor not in visited:
                            queue.append(neighbor)
            return subgraph
        isomorphic_subgraphs = []
        visited = set()
        for vertex in range(len(graph)):
            if vertex not in visited:
                subgraph = find_subgraph(graph, vertex)
                visited = visited.union(subgraph)
                is_isomorphic_subgraph = False
                for isomorphic_subgraph in isomorphic_subgraphs:
                    if is_isomorphic(subgraph, isomorphic_subgraph):
                        isomorphic_subgraph.update(subgraph)
                        is_isomorphic_subgraph = True
                        break
                if not is_isomorphic_subgraph:
                    isomorphic_subgraphs.append(subgraph)
        return len(isomorphic_subgraphs)
    graph = [[0, 1, 1, 0],
             [1, 0, 1, 1],
             [1, 1, 0, 0],
             [0, 1, 0, 0]]
    print(partition_into_isomorphic_subgraphs(graph))
