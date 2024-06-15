#Integral Flow With Bundles


    # Create a minimization problem

    # Decision variables

    # Objective function

    # Constraints

    # Bundle constraints

    # Capacity constraints

    # Solve the problem

    # Retrieve the solution

    # Return the objective value and flow dictionary

# Example usage:

# Add edges with capacities and costs

# Set the demands for nodes

# Set the bundle constraints



if __name__ == '__main__':
    from pulp import *
    def solve_integral_flow_with_bundles(graph, demands, bundle_constraints):
        prob = LpProblem("Integral Flow", LpMinimize)
        flow_vars = LpVariable.dicts("Flow", graph.edges(), lowBound=0, cat="Integer")
        prob += lpSum(flow_vars[edge] * graph[edge[0]][edge[1]]['cost'] for edge in graph.edges())
        for node in graph.nodes():
            inflow = lpSum(flow_vars[(i, node)] for i in graph.predecessors(node))
            outflow = lpSum(flow_vars[(node, j)] for j in graph.successors(node))
            prob += inflow - outflow == demands[node]
        for constraint in bundle_constraints:
            prob += lpSum(flow_vars[edge] for edge in constraint) <= 1
        for edge in graph.edges():
            prob += flow_vars[edge] <= graph[edge[0]][edge[1]]['capacity']
        prob.solve()
        flow_dict = {(edge[0], edge[1]): int(flow_vars[edge].varValue) for edge in graph.edges()}
        return value(prob.objective), flow_dict
    graph = nx.DiGraph()
    graph.add_edge('A', 'B', capacity=5, cost=2)
    graph.add_edge('A', 'C', capacity=3, cost=3)
    graph.add_edge('B', 'C', capacity=2, cost=1)
    graph.add_edge('B', 'D', capacity=4, cost=4)
    graph.add_edge('C', 'D', capacity=3, cost=2)
    demands = {'A': -5, 'D': 5}
    bundle_constraints = [[('A', 'B'), ('B', 'C')],
                          [('A', 'C')],
                          [('B', 'D')],
                          [('C', 'D')]]
    objective_value, flow_dict = solve_integral_flow_with_bundles(graph, demands, bundle_constraints)
    print("Objective Value:", objective_value)
    print("Flow on Edges:")
    for edge, flow in flow_dict.items():
        print(f"{edge[0]} -> {edge[1]}: {flow}")
