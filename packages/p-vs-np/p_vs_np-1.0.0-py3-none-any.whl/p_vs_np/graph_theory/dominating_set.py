#Dominating Set




if __name__ == '__main__':
    def dominating_set(graph, vertex, visited, dominating_set):
        visited.add(vertex)
        dominating_set.add(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                dominating_set.add(neighbor)
            dominating_set = dominating_set.union(dominating_set(graph, neighbor, visited, dominating_set))
        return dominating_set
    graph = {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2]}
    visited = set()
    dominating_set = set()
    print(dominating_set(graph, 0, visited, dominating_set))
