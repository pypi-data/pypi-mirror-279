#Strong Connectivity Augmentation










# Example usage:

if __name__ == '__main__':
    def is_strongly_connected(graph):
        n = len(graph)
        visited = [False] * n
        def dfs(u):
            visited[u] = True
            for v in range(n):
                if graph[u][v] and not visited[v]:
                    dfs(v)
        dfs(0)
        if all(visited):
            return True
        return False
    def strong_connectivity_augmentation(graph):
        n = len(graph)
        for u in range(n):
            for v in range(n):
                if u != v and not graph[u][v]:
                    graph[u][v] = 1
                    if not is_strongly_connected(graph):
                        return (u, v)
                    graph[u][v] = 0
        return None
    graph = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [1, 0, 0, 0]
    ]
    result = strong_connectivity_augmentation(graph)
    if result is None:
        print("The graph is already strongly connected.")
    else:
        u, v = result
        print("Add directed edge from vertex", u, "to vertex", v, "to achieve strong connectivity.")
