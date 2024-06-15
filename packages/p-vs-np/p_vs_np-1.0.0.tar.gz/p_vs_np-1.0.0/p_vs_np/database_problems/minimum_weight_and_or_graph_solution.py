#Minimum Weight and/or graph solution


    # Create a mapping of vertex IDs to their indices

    # Create a list of nodes for each vertex

    # Initialize the dynamic programming table

    # Build the dynamic programming table


    # Reconstruct the solution

    # Remove non-selected vertices from the graph


# Example usage
    # Example instance

    # Solve the "Minimum Weight and/or Graph Solution" problem

    # Print the subgraph

    # Print the selected nodes

if __name__ == '__main__':
    class Node:
        def __init__(self, vertex=None, weight=0, selected=False):
            self.vertex = vertex
            self.weight = weight
            self.selected = selected
    def minimum_weight_and_or_graph_solution(G, f, K):
        vertex_map = {vertex: i for i, vertex in enumerate(G)}
        nodes = [Node(vertex) for vertex in G]
        dp = [[None] * (K + 1) for _ in range(len(G))]
        for i, vertex in enumerate(G):
            for k in range(K + 1):
                if k == 0 or (f[vertex_map[vertex]] == 'and' and all(dp[j][k] is not None and dp[j][k].selected for j in G[vertex])):
                    dp[i][k] = Node(vertex, 0, True)
                elif f[vertex_map[vertex]] == 'or':
                    for j in G[vertex]:
                        if dp[j][k] is not None:
                            weight = sum(G[vertex][arc] for arc in G[vertex] if arc in G[j]) + dp[j][k].weight
                            if dp[i][k] is None or weight < dp[i][k].weight:
                                dp[i][k] = Node(vertex, weight, True)
                elif f[vertex_map[vertex]] == 'and':
                    for j in G[vertex]:
                        if dp[j][k - 1] is not None:
                            weight = sum(G[vertex][arc] for arc in G[vertex] if arc in G[j]) + dp[j][k - 1].weight
                            if dp[i][k] is None or weight < dp[i][k].weight:
                                dp[i][k] = Node(vertex, weight, True)
                if dp[i][k] is not None:
                    dp[i][k].selected = True
        solution = []
        selected_vertices = set()
        k = K
        for i in range(len(G)):
            if dp[i][k] is not None:
                node = dp[i][k]
                solution.append(node)
                selected_vertices.add(node.vertex)
                k -= node.weight
        subgraph = {vertex: {arc: weight for arc, weight in G[vertex].items() if arc in selected_vertices} for vertex in G if vertex in selected_vertices}
        return subgraph, solution
    if __name__ == '__main__':
        G = {
            's': {},
            'a': {'b': 1, 'c': 2},
            'b': {'d': 3},
            'c': {'d': 2},
            'd': {'e': 1},
            'e': {}
        }
        f = ['and', 'or', 'or', 'and', 'or']
        K = 6
        subgraph, solution = minimum_weight_and_or_graph_solution(G, f, K)
        print("Subgraph:")
        for vertex, arcs in subgraph.items():
            print(vertex, ':', arcs)
        print("Selected Nodes:")
        for node in solution:
            print(node)
