#Longest Circuit


    # Enumerate all simple cycles in the graph

    # Check if any cycle has a length of K or more


# Example usage:




if __name__ == '__main__':
    import networkx as nx
    def has_longest_circuit(graph, k):
        cycles = nx.simple_cycles(graph)
        for cycle in cycles:
            length = sum(graph[u][v]['weight'] for u, v in zip(cycle, cycle[1:] + [cycle[0]]))
            if length >= k:
                return True
        return False
    graph = nx.Graph()
    graph.add_edge('A', 'B', weight=2)
    graph.add_edge('B', 'C', weight=3)
    graph.add_edge('C', 'D', weight=4)
    graph.add_edge('D', 'A', weight=5)
    k = 10
    has_longest = has_longest_circuit(graph, k)
    print("Has Longest Circuit with length {} or more: {}".format(k, has_longest))
