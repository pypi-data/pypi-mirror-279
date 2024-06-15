#Travelling Salesman Polytope non - adjacency




    # Generate all possible pairs of non-adjacent vertices
            # Found a pair of non-adjacent vertices

    # No pair of non-adjacent vertices found


# Example usage



if __name__ == '__main__':
    import itertools
    def is_non_adjacent(graph):
        n = len(graph)
        for pair in itertools.combinations(range(n), 2):
            u, v = pair
            if not graph[u][v]:
                return True
        return False
    graph = [
        [False, True, True, True],
        [True, False, True, True],
        [True, True, False, True],
        [True, True, True, False]
    ]
    result = is_non_adjacent(graph)
    print(f"Does the Travelling Salesman Polytope have non-adjacent vertices? {result}")
