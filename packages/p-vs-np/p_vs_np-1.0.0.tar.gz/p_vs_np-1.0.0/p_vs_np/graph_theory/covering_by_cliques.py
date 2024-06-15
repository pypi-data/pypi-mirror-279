#Covering By Cliques





if __name__ == '__main__':
    def covering_by_cliques(graph):
        def find_clique(graph, vertex):
            clique = set()
            queue = [vertex]
            while queue:
                v = queue.pop(0)
                clique.add(v)
                for neighbor in graph[v]:
                    if neighbor not in clique and all(graph[neighbor][w] for w in clique):
                        queue.append(neighbor)
            return clique
        cliques = []
        visited = set()
        for vertex in range(len(graph)):
            if vertex not in visited:
                clique = find_clique(graph, vertex)
                visited = visited.union(clique)
                cliques.append(clique)
        return len(cliques)
    graph = [[0, 1, 1, 0],
             [1, 0, 1, 1],
             [1, 1, 0, 0],
             [0, 1, 0, 0]]
    print(covering_by_cliques(graph))
