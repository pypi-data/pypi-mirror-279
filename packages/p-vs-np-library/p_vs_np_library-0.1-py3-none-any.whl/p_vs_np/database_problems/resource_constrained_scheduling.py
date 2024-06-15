#Resource Constrained Scheduling

from collections import defaultdict


def list_scheduling(tasks, resource_constraints, task_durations):
    num_tasks = len(tasks)
    num_resources = len(resource_constraints)
    task_assignment = [None] * num_tasks
    resource_availability = [0] * num_resources

    # Assign tasks to processors using List Scheduling
    for task in tasks:
        min_available_resources = float('inf')
        selected_resource = None

        # Find the resource with the minimum availability that satisfies the task's constraints
        for resource in range(num_resources):
            if all(resource_availability[r] >= resource_constraints[task][r] for r in range(num_resources)):
                if resource_availability[resource] < min_available_resources:
                    min_available_resources = resource_availability[resource]
                    selected_resource = resource

        # Update task assignment and resource availability
        task_assignment[task] = selected_resource
        for resource in range(num_resources):
            resource_availability[resource] = max(0, resource_availability[resource] - resource_constraints[task][resource])
        for resource in range(num_resources):
            resource_availability[resource] += resource_constraints[task][resource]

    total_completion_time = max(resource_availability)

    return task_assignment, total_completion_time


# Example usage
if __name__ == "__main__":
    # Tasks and their durations
    tasks = [0, 1, 2, 3]
    task_durations = [4, 3, 2, 5]

    # Resource constraints for each task
    resource_constraints = {
        0: [2, 1, 0],  # Task 0 requires 2 units of resource 0, 1 unit of resource 1, and 0 units of resource 2
        1: [1, 2, 1],  # Task 1 requires 1 unit of resource 0, 2 units of resource 1, and 1 unit of resource 2
        2: [3, 0, 1],  # Task 2 requires 3 units of resource 0, 0 units of resource 1, and 1 unit of resource 2
        3: [1, 1, 2]   # Task 3 requires 1 unit of resource 0, 1 unit of resource 1, and 2 units of resource 2
    }

    task_assignment, total_completion_time = list_scheduling(tasks, resource_constraints, task_durations)

    print("Task Assignment:", task_assignment)
    print("Total Completion Time:", total_completion_time)
