#Fault Detection with test points




# Example usage
    # Example graph represented as an adjacency list

    # Example value of K

    # Find the fault detection set

    # Print the result


if __name__ == '__main__':
    from itertools import combinations
    def is_fault_detected(graph, test_points):
        for vertex in graph:
            if vertex not in test_points:
                for neighbor in graph[vertex]:
                    if neighbor not in test_points:
                        return False
        return True
    def find_fault_detection(graph, k):
        vertices = list(graph.keys())
        for i in range(1, k + 1):
            for test_points in combinations(vertices, i):
                if is_fault_detected(graph, test_points):
                    return test_points
        return None
    if __name__ == '__main__':
        graph = {
            's': ['a'],
            'a': ['b', 'c'],
            'b': ['d'],
            'c': ['d'],
            'd': ['e'],
            'e': ['f'],
            'f': ['g', 'h'],
            'g': ['i'],
            'h': ['i'],
            'i': ['j'],
            'j': ['l'],
            'l': ['1'],
            '1': []
        }
        k = 3
        fault_detection_set = find_fault_detection(graph, k)
        if fault_detection_set is not None:
            print("Faults can be detected with the following test points:", fault_detection_set)
        else:
            print("No fault detection set of size", k, "or less exists.")
