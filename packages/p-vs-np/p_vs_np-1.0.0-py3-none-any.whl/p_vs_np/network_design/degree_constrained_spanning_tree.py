#Degree Constrained Spanning Tree


    # initialize the graph

    # initialize the degree constraints

    # initialize the tree

    # initialize the queue

    # loop until the queue is empty
        # get the next vertex

        # check if the vertex can be added to the tree
            # update the degrees of the adjacent vertices

            # add the vertex to the tree

            # update the queue


if __name__ == '__main__':
    from collections import defaultdict
    def degree_constrained_spanning_tree(n, edges, degree_constraints):
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        degrees = {v: degree_constraints[v] for v in graph}
        tree = []
        queue = list(graph.keys())
        while queue:
            v = queue.pop(0)
            if degrees[v] > 0:
                for neighbor in graph[v]:
                    degrees[neighbor] -= 1
                tree.append((v, neighbor))
                queue.append(neighbor)
        return tree
