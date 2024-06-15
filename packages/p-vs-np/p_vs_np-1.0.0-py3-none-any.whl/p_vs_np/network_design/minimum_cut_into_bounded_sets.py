#Minimum Cut Into Bounded Sets








# Example usage:

if __name__ == '__main__':
    import itertools
    def min_cut_into_bounded_sets(graph, k):
        n = len(graph)
        min_cut_size = float('inf')
        for mask in range(1 << n):
            set_sizes = [0] * k
            cut_size = 0
            for u in range(n):
                set_sizes[(mask >> u) % k] += 1
            for u in range(n):
                for v in range(u + 1, n):
                    if (mask >> u) % k != (mask >> v) % k:
                        cut_size += graph[u][v]
            if all(size > 0 for size in set_sizes):
                min_cut_size = min(min_cut_size, cut_size)
        return min_cut_size
    graph = [
        [0, 1, 1, 0],
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [0, 1, 1, 0]
    ]
    k = 2
    result = min_cut_into_bounded_sets(graph, k)
    print("Minimum cut size into", k, "sets:", result)
