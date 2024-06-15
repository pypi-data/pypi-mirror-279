#Maximum Leaf Spanning Tree



    # initialize the graph

    # initialize the tree

    # initialize the queue

    # loop until the queue is empty
        # get the leaf with maximum degree

        # find its neighbor

        # remove the leaf from the graph

        # add the edge to the tree


if __name__ == '__main__':
    from collections import defaultdict
    def maximum_leaf_spanning_tree(n, edges):
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        tree = []
        queue = list(graph.keys())
        while queue:
            leaf = max(queue, key=lambda v: len(graph[v]))
            neighbor = graph[leaf][0]
            graph[neighbor].remove(leaf)
            queue.remove(leaf)
            tree.append((leaf, neighbor))
        return tree
