#Steiner Tree In Graphs





if __name__ == '__main__':
    def steiner_tree_in_graphs(n, edges, terminals):
        def find(u):
            if parents[u] != u:
                parents[u] = find(parents[u])
            return parents[u]
        def union(u, v):
            parents[find(u)] = find(v)
        def kruskal():
            edges.sort(key=lambda x: x[2])
            tree = []
            for u, v, w in edges:
                if find(u) != find(v):
                    union(u, v)
                    tree.append((u, v, w))
                    if len(tree) == n - 1:
                        return tree
            return tree
        parents = {i: i for i in terminals}
        return kruskal()
