#Graph K-Colourability (Chromatic Number)







if __name__ == '__main__':
    def is_safe(graph, vertex, color, c):
        for i in range(len(graph)):
            if graph[vertex][i] and c[i] == color:
                return False
        return True
    def k_colorable(graph, m, c, vertex, k):
        if vertex == len(graph):
            return True
        for color in range(1, k+1):
            if is_safe(graph, vertex, color, c):
                c[vertex] = color
                if k_colorable(graph, m, c, vertex+1, k):
                    return True
                c[vertex] = 0
        return False
    def chromatic_number(graph, k):
        c = [0 for i in range(len(graph))]
        if k_colorable(graph, len(graph), c, 0, k) == False:
            return False
        return True
    graph = [[0, 1, 1, 1],
             [1, 0, 1, 0],
             [1, 1, 0, 1],
             [1, 0, 1, 0]]
    k = 3
    if chromatic_number(graph, k) == True:
        print("Graph can be colored with k = ", k, "colors")
    else:
        print("Graph cannot be colored with given k value")
