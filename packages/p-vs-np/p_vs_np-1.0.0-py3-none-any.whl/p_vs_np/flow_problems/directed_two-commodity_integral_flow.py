#Directed Two-Commodity Integral Flow


    # Create a maximization problem

    # Decision variables

    # Objective function

    # Constraints

    # Capacity constraints

    # Solve the problem

    # Retrieve the solution

    # Return the objective value and flow dictionary

# Example usage:

# Add edges with capacities

# Set the demands for nodes

# Set the capacities for edges



if __name__ == '__main__':
    from pulp import *
    def solve_directed_two_commodity_integral_flow(graph, demands, capacities):
        prob = LpProblem("Directed Two-Commodity Flow", LpMaximize)
        flow_vars = LpVariable.dicts("Flow", graph.edges(), lowBound=0, cat="Integer")
        prob += lpSum(flow_vars[edge] for edge in graph.edges())
        for node in graph.nodes():
            inflow = lpSum(flow_vars[(i, node)] for i in graph.predecessors(node))
            outflow = lpSum(flow_vars[(node, j)] for j in graph.successors(node))
            prob += inflow - outflow == demands[node]
        for edge in graph.edges():
            prob += flow_vars[edge] <= capacities[edge]
        prob.solve()
        flow_dict = {(edge[0], edge[1]): int(flow_vars[edge].varValue) for edge in graph.edges()}
        return value(prob.objective), flow_dict
    graph = nx.DiGraph()
    graph.add_edge('A', 'B', capacity=5)
    graph.add_edge('A', 'C', capacity=3)
    graph.add_edge('B', 'C', capacity=2)
    graph.add_edge('B', 'D', capacity=4)
    graph.add_edge('C', 'D', capacity=3)
    demands = {'A': -5, 'D': 5}
    capacities = {('A', 'B'): 5, ('A', 'C'): 3, ('B', 'C'): 2, ('B', 'D'): 4, ('C', 'D'): 3}
    objective_value, flow_dict = solve_directed_two_commodity_integral_flow(graph, demands, capacities)
    print("Objective Value:", objective_value)
    print("Flow on Edges:")
    for edge, flow in flow_dict.items():
        print(f"{edge[0]} -> {edge[1]}: {flow}")
