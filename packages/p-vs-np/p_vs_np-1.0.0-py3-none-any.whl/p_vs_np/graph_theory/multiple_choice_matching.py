#Multiple Choice Matching


# Define the weight matrix

# Define the number of items and agents

# Define the constraints

# Define the bounds

# Solve the linear program

# Print the result

if __name__ == '__main__':
    from scipy.optimize import linprog
    weights = [[2, 4, 1], [3, 2, 4], [1, 3, 2], [4, 1, 3]]
    num_items = len(weights)
    num_agents = len(weights[0])
    c = [1 for i in range(num_items*num_agents)]
    A_eq = [[[1 if i == j else 0 for i in range(num_items) for j in range(num_agents)], [1 for i in range(num_items)]] for j in range(num_agents)]
    b_eq = [1 for i in range(num_agents)]
    bnds = [(0, 1) for i in range(num_items*num_agents)]
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bnds, method='simplex')
    print("Optimal value:", res.fun)
    print("Optimal solution:", res.x)
