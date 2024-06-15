#Hamiltonian Path






if __name__ == '__main__':
    def is_safe(v, graph, path, pos):
        if graph[path[pos-1]][v] == 0:
            return False
        for vertex in path:
            if vertex == v:
                return False
        return True
    def hamiltonian_path_util(graph, path, pos):
        if pos == V:
            return True
        for v in range(V):
            if is_safe(v, graph, path, pos):
                path[pos] = v
                if hamiltonian_path_util(graph, path, pos+1) == True:
                    return True
                path[pos] = -1
        return False
    def hamiltonian_path(graph):
        path = [-1] * V
        for i in range(V):
            path[0] = i
            if hamiltonian_path_util(graph, path, 1) == True:
                print("Hamiltonian path exists from vertex",i)
                print(path)
                return True
        print("Hamiltonian path does not exists")
        return False
    V = 5
    graph = [[0, 1, 0, 1, 0],
             [0, 0, 1, 1, 1],
             [0, 0, 0, 0, 1],
             [0, 0, 0, 0, 1],
             [0, 0, 0, 0, 0]]
    hamiltonian_path(graph)
