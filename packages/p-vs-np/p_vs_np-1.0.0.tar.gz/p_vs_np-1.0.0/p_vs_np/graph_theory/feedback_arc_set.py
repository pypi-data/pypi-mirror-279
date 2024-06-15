#Feedback Arc Set








if __name__ == '__main__':
    def feedback_arc_set(graph):
        def dfs(v, visited, adj_list):
            visited.add(v)
            for neighbor in adj_list[v]:
                if neighbor not in visited:
                    dfs(neighbor, visited, adj_list)
        def transpose(graph):
            t_graph = [[0 for _ in range(len(graph))] for _ in range(len(graph))]
            for i in range(len(graph)):
                for j in range(len(graph)):
                    t_graph[j][i] = graph[i][j]
            return t_graph
        def kosaraju(graph):
            visited = set()
            stack = []
            for vertex in range(len(graph)):
                if vertex not in visited:
                    dfs(vertex, visited, graph)
                    stack.append(vertex)
            feedback_arc_set = set()
            visited = set()
            t_graph = transpose(graph)
            while stack:
                vertex = stack.pop()
                if vertex not in visited:
                    component = []
                    dfs(vertex, visited, t_graph)
                    component.append(vertex)
                    for neighbor in component:
                        for vertex in component:
                            if graph[neighbor][vertex]:
                                feedback_arc_set.add((neighbor, vertex))
            return feedback_arc_set
    graph = [[0, 1, 1, 0],
             [0, 0, 0, 1],
             [0, 0, 0, 1],
             [0, 0, 0, 0]]
    print(feedback_arc_set(graph))
