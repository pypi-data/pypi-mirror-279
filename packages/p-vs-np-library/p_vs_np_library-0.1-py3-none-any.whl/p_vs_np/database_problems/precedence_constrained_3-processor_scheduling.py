#Precedence Constrained 3 - processor scheduling

import itertools


def is_valid_schedule(tasks, precedence, schedule, deadline):
    # Check precedence constraints
    for task1, task2 in precedence:
        if schedule[task1] >= schedule[task2]:
            return False

    # Check task count per time slot
    for time in range(deadline):
        count = sum(1 for task in tasks if schedule[task] == time)
        if count > 3:
            return False

    return True


def precedence_constrained_3_processor_scheduling(tasks, precedence, deadline):
    # Generate all possible schedules
    schedules = list(itertools.permutations(range(deadline), len(tasks)))

    # Check if each schedule satisfies the constraints
    for schedule in schedules:
        if is_valid_schedule(tasks, precedence, schedule, deadline):
            return True

    return False


# Example usage
if __name__ == '__main__':
    # Example instance
    tasks = {1, 2, 3, 4}
    precedence = [(1, 2), (3, 4)]
    deadline = 6

    # Solve the "Precedence Constrained 3-Processor Scheduling" problem
    result = precedence_constrained_3_processor_scheduling(tasks, precedence, deadline)

    # Print the result
    if result:
        print("Tasks can be scheduled on 3 processors satisfying the constraints")
    else:
        print("Tasks cannot be scheduled on 3 processors satisfying the constraints")

