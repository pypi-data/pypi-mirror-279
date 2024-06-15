#Multiple Choice Branching

        # compute a lower bound on the remaining weight
        # of the solution given the current state of the search




if __name__ == '__main__':
    def multiple_choice_branching(n, edges, weights, k):
        def bound(v, visited, size):
            bound = 0
            for neighbor, weight in graph[v]:
                if neighbor not in visited:
                    bound += weight
            return bound
        def dfs(v, visited, size):
            if size == k:
                return 0
            min_bound = float("inf")
            for neighbor, weight in graph[v]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    min_bound = min(min_bound, weight + dfs(neighbor, visited, size + 1))
                    visited.remove(neighbor)
            return min_bound
        graph = defaultdict(list)
        for u, v, w in edges:
            graph[u].append((v, w))
            graph[v].append((u, w))
        visited = set()
        visited.add(0)
        return dfs(0, visited, 0) + weights[0]
