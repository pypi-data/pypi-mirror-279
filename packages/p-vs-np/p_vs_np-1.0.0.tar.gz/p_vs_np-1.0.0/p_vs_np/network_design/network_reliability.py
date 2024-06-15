#Network Reliability





# Example usage:

if __name__ == '__main__':
    def network_reliability(graph, probabilities):
        n = len(graph)
        num_edges = sum(sum(row) for row in graph)
        total_reliability = 0
        def calculate_reliability(mask):
            reliability = 1
            for u in range(n):
                if (mask >> u) & 1:
                    for v in range(n):
                        if graph[u][v]:
                            reliability *= probabilities[u][v]
            return reliability
        for mask in range(1 << n):
            if bin(mask).count('1') == num_edges:
                reliability = calculate_reliability(mask)
                total_reliability += reliability
        return total_reliability
    graph = [
        [0, 1, 1, 0],
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [0, 1, 1, 0]
    ]
    probabilities = [
        [0.9, 0.8, 0.7, 0.6],
        [0.8, 0.9, 0.6, 0.5],
        [0.7, 0.6, 0.9, 0.4],
        [0.6, 0.5, 0.4, 0.9]
    ]
    result = network_reliability(graph, probabilities)
    print("Network reliability:", result)
