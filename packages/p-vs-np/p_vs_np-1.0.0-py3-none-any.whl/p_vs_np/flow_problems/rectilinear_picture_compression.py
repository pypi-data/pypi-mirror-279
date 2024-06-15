#Rectilinear






# Example usage


if __name__ == '__main__':
    picture
    compression
    def rectilinear_picture_compression(M, K):
        n = len(M)
        m = len(M[0])
        rectangles = []
        for i in range(n):
            for j in range(m):
                if M[i][j] == 1:
                    found_rectangle = False
                    for k in range(len(rectangles)):
                        a, b, c, d = rectangles[k]
                        if a <= i <= b and c <= j <= d:
                            found_rectangle = True
                            break
                    if not found_rectangle:
                        if len(rectangles) >= K:
                            return False
                        rectangles.append((i, i, j, j))
        return len(rectangles) <= K
    M = [
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 1, 1],
        [0, 0, 1, 1]
    ]
    K = 3
    result = rectilinear_picture_compression(M, K)
    if result:
        print("There exists a valid compression.")
    else:
        print("No valid compression exists.")
