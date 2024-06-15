#Bounded Diameter Spanning Tree


    # initialize the visited set

    # initialize the queue

    # loop until the queue is empty
        # get the next vertex

        # check if the vertex has been visited

        # add the vertex to the visited set

        # add the adjacent vertices to the queue

    # return the vertex and its distance from the source

    # find the minimum spanning tree

    # find the diameter of the minimum spanning tree

    # remove edges from the tree until the diameter is less than the bound


if __name__ == '__main__':
    from collections import defaultdict
    import heapq
    def find_diameter(graph, source):
        visited = set()
        queue = [(source, 0)]
        while queue:
            v, d = queue.pop(0)
            if v in visited:
                continue
            visited.add(v)
            for neighbor in graph[v]:
                queue.append((neighbor, d + 1))
        return v, d
    def bounded_diameter_spanning_tree(n, edges, bound):
        mst = kruskal(n, edges)
        graph = defaultdict(list)
        for u, v, w in mst:
            graph[u].append(v)
            graph[v].append(u)
        end1, diameter = find_diameter(graph, 0)
        end2, _ = find_diameter(graph, end1)
        while diameter > bound:
            for i in range(len(mst)):
                u, v, w = mst[i]
                if (u == end1 and v == end2) or (u == end2 and v == end1):
                    del mst[i]
                    break
            graph = defaultdict(list)
            for u, v, w in mst:
                graph[u].append(v)
                graph[v].append(u)
            end1, diameter = find_diameter(graph, 0)
            end2, _ = find_diameter(graph, end1)
        return mst
