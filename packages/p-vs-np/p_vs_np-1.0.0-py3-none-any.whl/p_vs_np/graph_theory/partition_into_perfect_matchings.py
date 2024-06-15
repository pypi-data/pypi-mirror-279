#Partition into Perfect Matchings





if __name__ == '__main__':
    def partition_into_perfect_matchings(graph):
        def find_perfect_matching(graph, vertex):
            perfect_matching = set()
            queue = [vertex]
            while queue:
                v = queue.pop(0)
                for neighbor in graph[v]:
                    if neighbor not in perfect_matching:
                        perfect_matching.add((v, neighbor))
                        queue.append(neighbor)
            return perfect_matching
        perfect_matchings = []
        visited = set()
        for vertex in range(len(graph)):
            if vertex not in visited:
                perfect_matching = find_perfect_matching(graph, vertex)
                visited = visited.union(set(x for match in perfect_matching for x in match))
                perfect_matchings.append(perfect_matching)
        return len(perfect_matchings)
    graph = [[0, 1, 1, 0],
             [1, 0, 1, 1],
             [1, 1, 0, 0],
             [0, 1, 0, 0]]
    print(partition_into_perfect_matchings(graph))
