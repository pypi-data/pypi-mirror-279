#Sparse Matrix Compression





# Example usage


if __name__ == '__main__':
    def sparse_matrix_compression(m, n):
        k = 0
        while True:
            sequence = generate_sequence(m, n, k)
            matrix = generate_matrix(m, n, sequence)
            if is_sparse_matrix(matrix):
                return sequence
            k += 1
    def generate_sequence(m, n, k):
        sequence = []
        for i in range(n + k):
            bi = i % m
            sequence.append(bi)
        return sequence
    def generate_matrix(m, n, sequence):
        matrix = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                val = i + sequence[i] + j
                if val % m == i:
                    matrix[i][j] = 1
        return matrix
    def is_sparse_matrix(matrix):
        row_counts = [sum(row) for row in matrix]
        col_counts = [sum(col) for col in zip(*matrix)]
        return max(row_counts) <= 1 and max(col_counts) <= 1
    m = 3
    n = 4
    sequence = sparse_matrix_compression(m, n)
    print("Sequence:", sequence)
