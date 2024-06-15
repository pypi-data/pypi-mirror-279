#Optimal Linear Arrangement


# Example pairwise distances between elements

# Create an instance of the Munkres class

# Solve the assignment problem and get the indices of the optimal linear arrangement

# Print the optimal linear arrangement

if __name__ == '__main__':
    import numpy as np
    from munkres import Munkres
    distances = np.array([[0, 10, 15, 20],
                         [10, 0, 35, 25],
                         [15, 35, 0, 30],
                         [20, 25, 30, 0]])
    munkres = Munkres()
    indices = munkres.compute(distances)
    print([i+1 for i, j in indices])
