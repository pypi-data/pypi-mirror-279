#Consecutive ones matrix partition







# Example usage


if __name__ == '__main__':
    def consecutive_ones_matrix_partition(matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        partitions = []
        def is_valid_partition(partition, submatrix):
            for p in partition:
                if has_overlap(p, submatrix):
                    return False
            return True
        def has_overlap(submatrix1, submatrix2):
            for r1, c1 in submatrix1:
                for r2, c2 in submatrix2:
                    if r1 == r2 or c1 == c2:
                        return True
            return False
        for r in range(rows):
            for c in range(cols):
                if matrix[r][c] == 1:
                    submatrix = [(r, c)]
                    for r2 in range(r + 1, rows):
                        if matrix[r2][c] == 1:
                            submatrix.append((r2, c))
                        else:
                            break
                    if is_valid_partition(partitions, submatrix):
                        partitions.append(submatrix)
        return partitions
    matrix = [
        [1, 0, 1, 1],
        [1, 1, 1, 0],
        [0, 1, 1, 1],
        [1, 1, 0, 0]
    ]
    partitions = consecutive_ones_matrix_partition(matrix)
    print("Partitions:")
    for partition in partitions:
        print(partition)
