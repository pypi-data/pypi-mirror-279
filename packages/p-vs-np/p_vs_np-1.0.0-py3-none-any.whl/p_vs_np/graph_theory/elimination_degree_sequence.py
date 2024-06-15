#Elimination Degree Sequence


    # Initialize the solution

    # Define a function to calculate the degree of violation of an element

    # Perform the greedy algorithm
        # Find the element with the minimum degree of violation
        # Append the element to the solution
        # Remove the element from the set of remaining elements

    # Return the solution


# Example usage


if __name__ == '__main__':
    def elimination_degree_sequence(elements, edges):
        solution = []
        def calculate_degree(element, position):
            degree = 0
            for tail, head in edges:
                if tail == element:
                    degree += position > solution.index(head)
            return degree
        while elements:
            element = min(elements, key=lambda e: calculate_degree(e, len(solution)))
            solution.append(element)
            elements.remove(element)
        return solution
    elements = [1, 2, 3, 4]
    edges = [(1, 2), (2, 3), (3, 4)]
    print(elimination_degree_sequence(elements, edges))
