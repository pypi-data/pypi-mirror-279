#Elimination Degree Sequence


def elimination_degree_sequence(elements, edges):
    # Initialize the solution
    solution = []

    # Define a function to calculate the degree of violation of an element
    def calculate_degree(element, position):
        degree = 0
        for tail, head in edges:
            if tail == element:
                degree += position > solution.index(head)
        return degree

    # Perform the greedy algorithm
    while elements:
        # Find the element with the minimum degree of violation
        element = min(elements, key=lambda e: calculate_degree(e, len(solution)))
        # Append the element to the solution
        solution.append(element)
        # Remove the element from the set of remaining elements
        elements.remove(element)

    # Return the solution
    return solution


# Example usage
elements = [1, 2, 3, 4]
edges = [(1, 2), (2, 3), (3, 4)]

print(elimination_degree_sequence(elements, edges))
