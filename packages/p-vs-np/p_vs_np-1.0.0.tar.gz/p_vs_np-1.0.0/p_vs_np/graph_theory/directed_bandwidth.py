#Directed Bandwidth





if __name__ == '__main__':
    from collections import defaultdict
    def bandwidth(graph,n):
        indegree = [0 for i in range(n)]
        for i in range(n):
            for j in range(n):
                if graph[i][j]:
                    indegree[j] += 1
        q = []
        for i in range(n):
            if indegree[i] == 0:
                q.append(i)
        top_sort = []
        while q:
            u = q.pop(0)
            top_sort.append(u)
            for v in range(n):
                if graph[u][v]:
                    indegree[v] -= 1
                    if indegree[v] == 0:
                        q.append(v)
        return top_sort
    graph = [[0, 1, 1, 1],
             [1, 0, 1, 0],
             [1, 1, 0, 1],
             [1, 0, 1, 0]]
    n = 4
    print(bandwidth(graph,n))
