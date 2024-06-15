#Fault Detection in Directed Graphs


    # Check if K > |I| * |O|

    # Generate all possible test sets of size K or less

    # Check if any test set can detect every single fault










# Example usage
    # Example instance


    # Solve the "FAULT DETECTION IN DIRECTED GRAPHS" problem

    # Print the result

if __name__ == '__main__':
    from itertools import combinations
    def fault_detection_in_directed_graphs(G, I, O, K):
        if K > len(I) * len(O):
            return True
        test_sets = []
        for k in range(K + 1):
            test_sets.extend(combinations(I, k))
        for test_set in test_sets:
            if is_fault_detected(G, test_set):
                return True
        return False
    def is_fault_detected(G, test_set):
        for v in G:
            for u1, u2 in test_set:
                if is_reachable(G, u1, u2, v):
                    break
            else:
                return False
        return True
    def is_reachable(G, u1, u2, v):
        stack = [u1]
        visited = set()
        while stack:
            current = stack.pop()
            if current == u2:
                return True
            visited.add(current)
            for neighbor in G[current]:
                if neighbor not in visited:
                    stack.append(neighbor)
        return False
    if __name__ == '__main__':
        G = {
            'v1': ['v2'],
            'v2': ['v3', 'v4'],
            'v3': ['v4'],
            'v4': []
        }
        I = ['v1']
        O = ['v4']
        K = 3
        result = fault_detection_in_directed_graphs(G, I, O, K)
        if result:
            print("Fault detected!")
        else:
            print("No fault detected!")
