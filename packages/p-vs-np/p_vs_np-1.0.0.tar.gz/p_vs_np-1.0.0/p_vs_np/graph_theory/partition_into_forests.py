#Partition Into Forests


        # check if the subgraph is a forest




if __name__ == '__main__':
    def partition_into_forests(graph):
        def dfs(v, visited, adj_list):
            visited.add(v)
            for neighbor in adj_list[v]:
                if neighbor not in visited:
                    dfs(neighbor, visited, adj_list)
        def is_forest(subgraph):
            return True
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
        visited = set()
        forests = []
        for vertex in range(len(graph)):
            if vertex not in visited:
                subgraph = find_subgraph(graph, vertex)
                visited = visited.union(subgraph)
                if is_forest(subgraph):
                    forests.append(subgraph)
        return len(forests)
    graph = [[0, 1, 1, 0],
             [1, 0, 1, 1],
             [1, 1, 0, 0],
             [0, 1, 0, 0]]
    print(partition_into_forests(graph))
