#Clustering










# Example usage
    # Define your distance function here





if __name__ == '__main__':
    import itertools
    def is_valid_clustering(X, clusters, B):
        for cluster in clusters:
            for x, y in itertools.combinations(cluster, 2):
                if distance(x, y) > B:
                    return False
        return True
    def clustering(X, K, B):
        n = len(X)
        best_clustering = None
        min_max_distance = float('inf')
        for combination in itertools.combinations(X, K):
            clusters = [list(combination)]
            remaining_points = set(X) - set(combination)
            for point in remaining_points:
                min_distance = float('inf')
                min_cluster = None
                for i, cluster in enumerate(clusters):
                    max_distance = max(distance(point, p) for p in cluster)
                    if max_distance < min_distance:
                        min_distance = max_distance
                        min_cluster = i
                if min_distance <= B:
                    clusters[min_cluster].append(point)
                else:
                    clusters.append([point])
            if is_valid_clustering(X, clusters, B):
                max_distance = max(max(distance(x, y) for x, y in itertools.combinations(cluster, 2)) for cluster in clusters)
                if max_distance < min_max_distance:
                    min_max_distance = max_distance
                    best_clustering = clusters
        return best_clustering
    def distance(x, y):
        return abs(x - y)
    X = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    K = 3
    B = 2
    best_clustering = clustering(X, K, B)
    print("Best Clustering:")
    for i, cluster in enumerate(best_clustering, start=1):
        print(f"Cluster {i}: {cluster}")
