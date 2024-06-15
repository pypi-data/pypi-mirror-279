#Biconnectivity Augmentation












# Example usage:


if __name__ == '__main__':
    def is_biconnected(graph):
        n = len(graph)
        visited = [False] * n
        disc = [float('inf')] * n
        low = [float('inf')] * n
        parent = [-1] * n
        time = 0
        def dfs(u):
            nonlocal time
            visited[u] = True
            disc[u] = time
            low[u] = time
            time += 1
            for v in range(n):
                if graph[u][v]:
                    if not visited[v]:
                        parent[v] = u
                        dfs(v)
                        low[u] = min(low[u], low[v])
                        if low[v] > disc[u]:
                            return False
                    elif parent[u] != v:
                        low[u] = min(low[u], disc[v])
            return True
        for v in range(n):
            if not visited[v] and not dfs(v):
                return False
        return True
    def biconnectivity_augmentation(graph):
        n = len(graph)
        for u in range(n):
            for v in range(u + 1, n):
                if not graph[u][v]:
                    graph[u][v] = 1
                    graph[v][u] = 1
                    if not is_biconnected(graph):
                        return (u, v)
                    graph[u][v] = 0
                    graph[v][u] = 0
        return None
    graph = [
        [0, 1, 0, 0, 1],
        [1, 0, 1, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 1, 0, 0],
        [1, 0, 0, 0, 0]
    ]
    result = biconnectivity_augmentation(graph)
    if result is None:
        print("The graph is already biconnected.")
    else:
        u, v = result
        print("Add edge between vertices", u, "and", v, "to achieve biconnectivity.")
