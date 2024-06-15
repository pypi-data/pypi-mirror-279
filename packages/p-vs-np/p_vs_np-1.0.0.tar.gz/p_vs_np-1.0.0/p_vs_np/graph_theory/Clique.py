#Clique





# Print the largest clique

if __name__ == '__main__':
    def BronKerbosch(R, P, X, graph, cliques):
        if not P and not X:
            cliques.append(R)
            return
        for vertex in P.copy():
            BronKerbosch(R.union([vertex]), P.intersection(graph[vertex]), X.intersection(graph[vertex]), graph, cliques)
            P.remove(vertex)
            X.add(vertex)
    def find_cliques(graph):
        cliques = []
        BronKerbosch(set(), set(graph.keys()), set(), graph, cliques)
        return cliques
    graph = {
        0: {1, 2},
        1: {0, 2},
        2: {0, 1, 3},
        3: {2},
        4: {5, 6},
        5: {4, 6},
        6: {4, 5}
    }
    cliques = find_cliques(graph)
    max_clique = max(cliques, key=lambda x: len(x))
    print(max_clique)
