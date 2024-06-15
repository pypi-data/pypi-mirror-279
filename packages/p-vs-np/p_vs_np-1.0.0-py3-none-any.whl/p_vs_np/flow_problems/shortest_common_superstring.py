#Shortest Common Superstring

    # Create an overlap graph between the strings

    # Find the Hamiltonian path in the overlap graph

    # Construct the shortest common superstring



















# Example usage


if __name__ == '__main__':
    def find_shortest_common_superstring(strings):
        overlap_graph = create_overlap_graph(strings)
        path = find_hamiltonian_path(overlap_graph)
        superstring = reconstruct_superstring(strings, path)
        return superstring
    def create_overlap_graph(strings):
        n = len(strings)
        overlap_graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    overlap_graph[i][j] = calculate_overlap(strings[i], strings[j])
        return overlap_graph
    def calculate_overlap(s1, s2):
        max_overlap = 0
        for i in range(1, min(len(s1), len(s2))):
            if s1[-i:] == s2[:i]:
                max_overlap = i
        return max_overlap
    def find_hamiltonian_path(graph):
        n = len(graph)
        visited = [False] * n
        path = []
        def dfs(node):
            visited[node] = True
            path.append(node)
            if len(path) == n:
                return True
            for neighbor in range(n):
                if graph[node][neighbor] > 0 and not visited[neighbor]:
                    if dfs(neighbor):
                        return True
            visited[node] = False
            path.pop()
            return False
        for start_node in range(n):
            if dfs(start_node):
                break
        return path
    def reconstruct_superstring(strings, path):
        superstring = strings[path[0]]
        for i in range(1, len(path)):
            overlap = calculate_overlap(strings[path[i-1]], strings[path[i]])
            superstring += strings[path[i]][overlap:]
        return superstring
    strings = ["cat", "act", "tac", "dog", "god"]
    result = find_shortest_common_superstring(strings)
    print("Shortest Common Superstring:", result)
