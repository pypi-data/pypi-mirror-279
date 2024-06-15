#Bounded Component Spanning Tree





if __name__ == '__main__':
    from collections import defaultdict
    def bounded_component_spanning_tree(n, edges, bound):
        graph = defaultdict(list)
        for u, v, w in edges:
            graph[u].append((v, w))
            graph[v].append((u, w))
        def dfs(v, visited, size):
            visited.add(v)
            for neighbor, weight in graph[v]:
                if neighbor not in visited:
                    if size + 1 <= bound:
                        size += 1
                        dfs(neighbor, visited, size)
                    else:
                        break
            return size
        tree = []
        visited = set()
        for v in range(n):
            if v not in visited:
                size = dfs(v, visited, 0)
                if size < bound:
                    for neighbor, weight in graph[v]:
                        if neighbor not in visited:
                            tree.append((v, neighbor, weight))
                            break
        return tree
