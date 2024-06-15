#Feedback Vertex Set






if __name__ == '__main__':
    def feedback_vertex_set(graph):
        def dfs(v, visited, adj_list):
            visited.add(v)
            for neighbor in adj_list[v]:
                if neighbor not in visited:
                    dfs(neighbor, visited, adj_list)
        def has_cycle(adj_list):
            visited = set()
            for v in range(len(adj_list)):
                if v not in visited:
                    stack = [v]
                    while stack:
                        vertex = stack.pop()
                        visited.add(vertex)
                        for neighbor in adj_list[vertex]:
                            if neighbor not in visited:
                                stack.append(neighbor)
                            elif neighbor in stack:
                                return True
            return False
        def kernelization(graph, feedback_vertex_set):
            adj_list = {i: set() for i in range(len(graph))}
            for i in range(len(graph)):
                for j in range(i, len(graph)):
                    if graph[i][j] and i not in feedback_vertex_set and j not in feedback_vertex_set:
                        adj_list[i].add(j)
                        adj_list[j].add(i)
            return adj_list
        feedback_vertex_set = set()
        while has_cycle(graph):
            vertex = 0
            for i in range(len(graph)):
                if sum(graph[i]) > sum(graph[vertex]):
                    vertex = i
            feedback_vertex_set.add(vertex)
            graph = kernelization(graph, feedback_vertex_set)
        return feedback_vertex_set
    graph = [[0, 1, 1, 0],
             [1, 0, 0, 1],
             [1, 0, 0, 1],
             [0, 1, 1, 0]]
    print(feedback_vertex_set(graph))
