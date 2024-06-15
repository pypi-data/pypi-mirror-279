#Independent Set



    # Constraint: no two adjacent vertices can be in the independent set




if __name__ == '__main__':
    from gurobipy import *
    def independent_set(graph):
        model = Model("independent_set")
        vertex_count = len(graph)
        vertices = [i for i in range(vertex_count)]
        x = model.addVars(vertices, vtype=GRB.BINARY, name="x")
        model.setObjective(quicksum(x[i] for i in vertices), GRB.MAXIMIZE)
        for i in range(vertex_count):
            for j in range(i+1, vertex_count):
                if graph[i][j] == 1:
                    model.addConstr(x[i] + x[j] <= 1)
        model.optimize()
        return [v for v in vertices if x[v].x == 1]
    graph = [[0, 1, 1, 0],
             [1, 0, 1, 1],
             [1, 1, 0, 0],
             [0, 1, 0, 0]]
    print(independent_set(graph))
