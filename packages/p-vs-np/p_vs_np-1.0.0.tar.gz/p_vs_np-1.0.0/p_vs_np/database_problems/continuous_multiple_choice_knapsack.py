#Continuous Multiple Choice Knapsack



    # Create decision variables

    # Set objective function

    # Add weight constraint

    # Solve the problem

    # Retrieve the optimal solution


# Example usage



if __name__ == '__main__':
    from pulp import LpProblem, LpVariable, LpMaximize
    def knapsack_continuous(items, capacity):
        problem = LpProblem("Continuous Knapsack", LpMaximize)
        x = [LpVariable(f"x{i}", lowBound=0, upBound=1, cat="Continuous") for i in range(len(items))]
        problem += sum(x[i] * items[i][1] for i in range(len(items)))
        problem += sum(x[i] * items[i][0] for i in range(len(items))) <= capacity
        problem.solve()
        max_value = problem.objective.value()
        included_items = [(items[i][0], items[i][1], x[i].value()) for i in range(len(items)) if x[i].value() > 0]
        return max_value, included_items
    items = [(2, 10), (3, 15), (5, 20), (7, 25)]  # (weight, value) pairs
    capacity = 10
    max_value, included_items = knapsack_continuous(items, capacity)
    print("Maximum value:", max_value)
    print("Included items:")
    for item in included_items:
        print(f"Weight: {item[0]}, Value: {item[1]}, Fraction: {item[2]}")
