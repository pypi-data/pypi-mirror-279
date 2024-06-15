#Production Planning



    # Create the LP problem

    # Decision variables

    # Objective function: maximize profit

    # Constraints


    # Solve the problem

    # Print the solution


# Example usage
    # List of products

    # List of resources

    # Demands for each product

    # Production capacities for each resource

    # Production costs for each product and resource

    # Profits for each product

    # Solve the production planning problem


if __name__ == '__main__':
    from pulp import LpProblem, LpVariable, LpMaximize, LpStatus, lpSum
    def production_planning(products, resources, demands, capacities, costs, profits):
        problem = LpProblem("Production Planning", LpMaximize)
        production = LpVariable.dicts("Production", products, lowBound=0, cat="Integer")
        problem += lpSum(profits[i] * production[i] for i in products)
        for r in resources:
            problem += lpSum(costs[i][r] * production[i] for i in products) <= capacities[r]
        for d in demands:
            problem += lpSum(production[i] for i in products if i in demands[d]) >= demands[d]
        problem.solve()
        if problem.status == LpStatusOptimal:
            print("Production quantities:")
            for i in products:
                print(f"{i}: {production[i].varValue}")
            print("Total Profit: ", lpSum(profits[i] * production[i].varValue for i in products))
        else:
            print("No feasible solution found.")
    if __name__ == "__main__":
        products = ["Product1", "Product2", "Product3"]
        resources = ["Resource1", "Resource2"]
        demands = {
            "Demand1": ["Product1", "Product2"],
            "Demand2": ["Product1", "Product3"],
        }
        capacities = {
            "Resource1": 100,
            "Resource2": 200,
        }
        costs = {
            "Product1": {"Resource1": 10, "Resource2": 20},
            "Product2": {"Resource1": 15, "Resource2": 25},
            "Product3": {"Resource1": 20, "Resource2": 30},
        }
        profits = {
            "Product1": 50,
            "Product2": 60,
            "Product3": 70,
        }
        production_planning(products, resources, demands, capacities, costs, profits)
