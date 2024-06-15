#Geometric Connected Dominating Set


    # Create a graph and add nodes

    # Add edges based on adjacency within radius

    # Find the connected dominating set



# Example usage:


# Print the dominating set

# Visualize the graph and dominating set

if __name__ == '__main__':
    import networkx as nx
    import matplotlib.pyplot as plt
    def find_geometric_connected_dominating_set(points, radius):
        graph = nx.Graph()
        for i, point in enumerate(points):
            graph.add_node(i, pos=point)
        for i, point1 in enumerate(points):
            for j, point2 in enumerate(points):
                if i != j and distance(point1, point2) <= radius:
                    graph.add_edge(i, j)
        dominating_set = nx.dominating_set(graph)
        return dominating_set
    def distance(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    points = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
    radius = 2
    dominating_set = find_geometric_connected_dominating_set(points, radius)
    print("Dominating Set:", dominating_set)
    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw(graph, pos=pos, with_labels=True)
    plt.scatter(*zip(*points), color='r')
    plt.scatter(*zip(*[points[i] for i in dominating_set]), color='g')
    plt.show()
