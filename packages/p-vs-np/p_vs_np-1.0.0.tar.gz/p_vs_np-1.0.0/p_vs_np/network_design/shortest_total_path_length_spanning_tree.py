#Shortest Total Path Length Spanning Tree


    # initialize the graph

    # initialize the tree

    # initialize the priority queue

    # initialize the visited set

    # loop until the queue is empty
        # get the next vertex

        # check if the vertex has been visited

        # add the vertex to the visited set

        # add the edge to the tree

        # add the adjacent vertices to the queue


if __name__ == '__main__':
    from collections import defaultdict
    import heapq
    def prim(n, edges):
        graph = defaultdict(list)
        for u, v, w in edges:
            graph[u].append((v, w))
            graph[v].append((u, w))
        tree = []
        queue = [(0, 0, -1)]
        visited = set()
        while queue:
            w, u, p = heapq.heappop(queue)
            if u in visited:
                continue
            visited.add(u)
            if p != -1:
                tree.append((p, u, w))
            for v, w in graph[u]:
                if v not in visited:
                    heapq.heappush(queue, (w, v, u))
        return tree
