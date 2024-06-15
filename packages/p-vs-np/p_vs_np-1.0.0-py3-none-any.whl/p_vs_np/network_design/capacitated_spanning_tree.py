#Capacitated Spanning Tree


    # Create the LP problem

    # Create the binary decision variables

    # Create the objective function

    # Add the degree constraints

    # Add the capacity constraints

    # Solve the LP problem

    # Extract the solution

if __name__ == '__main__':
    from pulp import *
    def capacitated_spanning_tree(n, edges, capacity):
        prob = LpProblem("Capacitated Spanning Tree", LpMinimize)
        x = {(u, v): LpVariable(f"x_{u}_{v}", 0, 1, LpBinary) for u, v, w in edges}
        prob += lpSum([x[u, v] * w for u, v, w in edges]), "Total Edge Weight"
        for i in range(n):
            prob += lpSum([x[u, v] for u, v in x.keys() if u == i]) == 2, f"Degree of {i}"
        for u, v, w in edges:
            prob += x[u,v] * w <= capacity
        prob.solve()
        tree = [(u, v) for u, v in x.keys() if x[u, v].value() == 1.0]
        return tree
