#Longest Path


    # Find all simple paths from source to target

    # Check if any path has a length of K or more


# Example usage:



if __name__ == '__main__':
    import networkx as nx
    def has_longest_path(graph, source, target, k):
        paths = nx.all_simple_paths(graph, source, target)
        for path in paths:
            length = sum(graph[u][v]['weight'] for u, v in zip(path, path[1:]))
            if length >= k:
                return True
        return False
    graph = nx.DiGraph()
    graph.add_edge('A', 'B', weight=2)
    graph.add_edge('B', 'C', weight=3)
    graph.add_edge('C', 'D', weight=4)
    graph.add_edge('D', 'A', weight=5)
    source = 'A'
    target = 'D'
    k = 10
    has_longest = has_longest_path(graph, source, target, k)
    print("Has Longest Path from {} to {} with length {} or more: {}".format(source, target, k, has_longest))
