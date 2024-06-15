#Knapsack


    # Create a table to store the maximum values for different subproblems


    # Find the items included in the knapsack


# Example usage


if __name__ == '__main__':
    def knapsack(items, capacity):
        n = len(items)
        table = [[0] * (capacity + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            weight, value = items[i - 1]
            for j in range(1, capacity + 1):
                if weight > j:
                    table[i][j] = table[i - 1][j]
                else:
                    table[i][j] = max(table[i - 1][j], value + table[i - 1][j - weight])
        included_items = []
        j = capacity
        for i in range(n, 0, -1):
            if table[i][j] != table[i - 1][j]:
                weight, value = items[i - 1]
                included_items.append((weight, value))
                j -= weight
        return table[n][capacity], included_items
    items = [(2, 10), (3, 15), (5, 20), (7, 25)]  # (weight, value) pairs
    capacity = 10
    max_value, included_items = knapsack(items, capacity)
    print("Maximum value:", max_value)
    print("Included items:", included_items)
