#Network Survivability






# Example usage:


if __name__ == '__main__':
    import itertools
    def is_k_vertex_connected(graph, k):
        n = len(graph)
        for subset in itertools.combinations(range(n), k):
            visited = [False] * n
            stack = [subset[0]]
            visited[subset[0]] = True
            while stack:
                u = stack.pop()
                for v in range(n):
                    if graph[u][v] and not visited[v] and v in subset:
                        stack.append(v)
                        visited[v] = True
            if not all(visited[v] for v in subset):
                return False
        return True
    graph = [
        [0, 1, 1, 0],
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [0, 1, 1, 0]
    ]
    k = 2
    result = is_k_vertex_connected(graph, k)
    if result:
        print(f"The graph is {k}-vertex connected.")
    else:
        print(f"The graph is not {k}-vertex connected.")
