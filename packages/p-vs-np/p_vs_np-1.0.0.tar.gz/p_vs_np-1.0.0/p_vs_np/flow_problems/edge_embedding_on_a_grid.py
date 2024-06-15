#Edge Embedding On A Grid










# Example usage:




if __name__ == '__main__':
    def check_edge_embedding(graph):
        n = len(graph)
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1 and not can_embed_edges(graph, i, j):
                    return False
        return True
    def can_embed_edges(graph, source, target):
        visited = set()
        stack = [(source, -1)]
        while stack:
            node, parent = stack.pop()
            if node == target:
                return True
            visited.add(node)
            for neighbor in range(len(graph[node])):
                if graph[node][neighbor] == 1 and neighbor != parent:
                    if neighbor in visited:
                        return False
                    stack.append((neighbor, node))
        return False
    graph = [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0]
    ]
    embeddable = check_edge_embedding(graph)
    if embeddable:
        print("Graph can be embedded on a grid without crossing edges")
    else:
        print("Graph cannot be embedded on a grid without crossing edges")
