#Fault Detection in Logic Circuits



    # Initialize the output dictionary

    # Check if V' contains a single vertex y with f(y) = 1

    # Create a mapping of vertex IDs to their indices

    # Add the stuck-at-x assignment for each vertex in V'

    # Enumerate all possible input/output assignments

        # Check if the circuit output differs from the stuck-at-x output for any input assignment



    # Perform a depth-first search to compute the output of the circuit









    # Check if the output of the circuit differs from the stuck-at-x output


# Example usage
    # Example instance



    # Solve the "FAULT DETECTION IN LOGIC CIRCUITS" problem

    # Print the result

if __name__ == '__main__':
    from itertools import product
    class Vertex:
        def __init__(self, value=None, in_deg=0):
            self.value = value
            self.in_deg = in_deg
    def fault_detection_in_logic_circuits(G, V_prime):
        output = {}
        if len(V_prime) == 1 and G[V_prime[0]].value == 1:
            return False
        vertex_map = {vertex: i for i, vertex in enumerate(G)}
        for vertex in V_prime:
            output[vertex] = 'x'
        for assignment in product(['T', 'F'], repeat=len(V_prime)):
            for i, vertex in enumerate(V_prime):
                output[vertex] = assignment[i]
            if is_fault_detected(G, output):
                return True
        return False
    def is_fault_detected(G, output):
        stack = []
        visited = set()
        for vertex in G:
            if vertex not in visited:
                stack.append(vertex)
                while stack:
                    current = stack.pop()
                    if current in visited:
                        continue
                    visited.add(current)
                    if current in output:
                        G[current].value = output[current]
                    if G[current].value == 'x':
                        continue
                    in_deg = G[current].in_deg
                    if G[current].value == 1 and in_deg > 0:
                        continue
                    for neighbor in G[current].neighbors:
                        G[neighbor].in_deg -= 1
                        if G[neighbor].in_deg == 0:
                            stack.append(neighbor)
        for vertex in G:
            if vertex not in output and G[vertex].value != 'x':
                return True
        return False
    if __name__ == '__main__':
        G = {
            'x1': Vertex('or', 2),
            'x2': Vertex('and', 2),
            'x3': Vertex('not', 1),
            'x4': Vertex(1, 0),
            'x5': Vertex(0, 1),
            'x6': Vertex(1, 1),
            'y': Vertex('or', 2)
        }
        G['x1'].neighbors = ['x3', 'x4']
        G['x2'].neighbors = ['x3', 'x5']
        G['x3'].neighbors = ['x6']
        G['x4'].neighbors = ['y']
        G['x5'].neighbors = ['y']
        G['x6'].neighbors = ['y']
        G['y'].neighbors = []
        V_prime = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6']
        result = fault_detection_in_logic_circuits(G, V_prime)
        if result:
            print("Fault detected!")
        else:
            print("No fault detected!")
