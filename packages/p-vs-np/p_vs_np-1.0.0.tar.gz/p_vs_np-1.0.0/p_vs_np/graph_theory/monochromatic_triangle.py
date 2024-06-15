#Monochromatic Triangle




if __name__ == '__main__':
    def monochromatic_triangle(graph, color_map):
        for vertex1 in range(len(graph)):
            for vertex2 in range(vertex1 + 1, len(graph)):
                if graph[vertex1][vertex2] and color_map[vertex1] == color_map[vertex2]:
                    for vertex3 in range(vertex2 + 1, len(graph)):
                        if graph[vertex1][vertex3] and graph[vertex2][vertex3] and color_map[vertex1] == color_map[vertex3]:
                            return True
        return False
    graph = [[0, 1, 1, 1],
             [1, 0, 1, 0],
             [1, 1, 0, 1],
             [1, 0, 1, 0]]
    color_map = [1, 2, 1, 3]
    if monochromatic_triangle(graph, color_map) == True:
        print("Graph has a monochromatic triangle.")
    else:
        print("Graph does not have a monochromatic triangle.")
