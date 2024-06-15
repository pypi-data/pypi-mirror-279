#Minimum Broadcast Time



    # Breadth-First Search (BFS)




# Example usage:





if __name__ == '__main__':
    import networkx as nx
    def calculate_minimum_broadcast_time(graph, source):
        distances = {node: float('inf') for node in graph.nodes}
        distances[source] = 0
        queue = [source]
        while queue:
            node = queue.pop(0)
            for neighbor in graph.neighbors(node):
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = distances[node] + 1
                    queue.append(neighbor)
        return max(distances.values())
    graph = nx.Graph()
    graph.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4)])
    source_node = 1
    minimum_broadcast_time = calculate_minimum_broadcast_time(graph, source_node)
    print("Minimum Broadcast Time:", minimum_broadcast_time)
