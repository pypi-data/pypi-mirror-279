#Capacity Assignment






# Example usage





if __name__ == '__main__':
    def is_capacity_assignment_possible(graph, source, sink, capacities):
        visited = set()
        return dfs(graph, source, sink, capacities, visited)
    def dfs(graph, node, sink, capacities, visited):
        if node == sink:
            return True
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited and capacities[(node, neighbor)] > 0:
                if dfs(graph, neighbor, sink, capacities, visited):
                    return True
        return False
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['D', 'E'],
        'D': ['F'],
        'E': ['F'],
        'F': []
    }
    capacities = {
        ('A', 'B'): 2,
        ('A', 'C'): 3,
        ('B', 'D'): 1,
        ('B', 'E'): 1,
        ('C', 'D'): 2,
        ('C', 'E'): 2,
        ('D', 'F'): 2,
        ('E', 'F'): 3
    }
    source = 'A'
    sink = 'F'
    result = is_capacity_assignment_possible(graph, source, sink, capacities)
    if result:
        print("Capacity assignment is possible.")
    else:
        print("Capacity assignment is not possible.")
