#Graph Partition


        # compute the difference in the size of the partition
        # if u were to be moved to the other partition






if __name__ == '__main__':
    from collections import defaultdict
    def graph_partition(n, edges, k):
        def gain(u, partition):
            current_size = sum(1 for v in graph[u] if v in partition)
            return current_size - (degrees[u] - current_size)
        def swap(u, v):
            partition_u = partitions[u]
            partition_v = partitions[v]
            partitions[u] = partition_v
            partitions[v] = partition_u
            gains[u] = gain(u, partition_v)
            gains[v] = gain(v, partition_u)
        def find_max_gain_vertex(partition):
            max_gain = float("-inf")
            max_vertex = None
            for vertex in partition:
                if gains[vertex] > max_gain:
                    max_gain = gains[vertex]
                    max_vertex = vertex
            return max_vertex
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        degrees = {vertex: len(
        graph[vertex]) for vertex in graph}
        partitions = {i: i < k for i in range(n)}
        gains = {vertex: gain(vertex, partitions[vertex]) for vertex in graph}
        while True:
            u = find_max_gain_vertex(partitions[True])
            v = find_max_gain_vertex(partitions[False])
            if gains[u] + gains[v] < 0:
                break
            swap(u, v)
        return partitions
