#Bounded Post Correspondence Problem

def solve_bounded_post_correspondence_problem(dominos, bound):
    stack = [(("", ""), 0)]  # Stack to store partial solutions
    solution = None  # Variable to store the final solution

    while stack:
        (seq1, seq2), steps = stack.pop()

        if steps > bound:
            continue

        if seq1 == seq2:
            solution = (seq1, seq2)
            break

        for domino in dominos:
            new_seq1 = seq1 + domino[0]
            new_seq2 = seq2 + domino[1]
            stack.append(((new_seq1, new_seq2), steps + 1))

    if solution:
        return f"A valid solution exists within {bound} steps: {solution[0]} = {solution[1]}"
    else:
        return f"No valid solution found within {bound} steps"

# Example usage
dominos = [("ab", "ba"), ("a", "b")]
bound = 10

result = solve_bounded_post_correspondence_problem(dominos, bound)
print(result)
