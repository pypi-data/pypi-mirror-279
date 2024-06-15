##Vertex Cover

    # Function to check if the given set of vertices is a vertex cover

    # Recursive function to find all possible vertex covers


# Example usage

if __name__ == '__main__':
    def is_vertex_cover(graph, vertex_cover):
        for edge in graph:
            if edge[0] not in vertex_cover and edge[1] not in vertex_cover:
                return False
        return True
    def vertex_cover(graph, vertex_cover=[]):
        if not graph:
            if is_vertex_cover(graph, vertex_cover):
                print(vertex_cover)
            return
        vertex_cover.append(graph[0][0])
        vertex_cover(graph[1:], vertex_cover)
        vertex_cover.pop()
        vertex_cover.append(graph[0][1])
        vertex_cover(graph[1:], vertex_cover)
        vertex_cover.pop()
    graph = [(1, 2), (1, 3), (2, 3), (4, 5)]
    vertex_cover(graph)
