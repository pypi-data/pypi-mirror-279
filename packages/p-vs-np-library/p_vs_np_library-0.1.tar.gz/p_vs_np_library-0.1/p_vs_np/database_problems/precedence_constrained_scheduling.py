#Precedence Constrained Scheduling

from collections import defaultdict, deque


def topological_sort(graph):
    in_degrees = defaultdict(int)
    sorted_order = []
    queue = deque()

    # Calculate in-degrees for each task
    for u in graph:
        for v in graph[u]:
            in_degrees[v] += 1

    # Add tasks with no dependencies to the queue
    for u in graph:
        if in_degrees[u] == 0:
            queue.append(u)

    # Perform topological sorting
    while queue:
        u = queue.popleft()
        sorted_order.append(u)

        for v in graph[u]:
            in_degrees[v] -= 1
            if in_degrees[v] == 0:
                queue.append(v)

    # Check for a cycle (if any remaining tasks with positive in-degree)
    for u in graph:
        if in_degrees[u] > 0:
            return None

    return sorted_order


def list_scheduling(tasks, precedence_constraints, task_processing_times):
    num_tasks = len(tasks)
    task_assignment = [None] * num_tasks
    processor_loads = [0] * len(task_processing_times)

    # Sort tasks based on the topological order
    sorted_tasks = topological_sort(precedence_constraints)

    # Assign tasks to processors using List Scheduling
    for task in sorted_tasks:
        min_load = min(processor_loads)
        min_load_processor = processor_loads.index(min_load)

        task_assignment[task] = min_load_processor
        processor_loads[min_load_processor] += task_processing_times[task]

    total_completion_time = max(processor_loads)

    return task_assignment, total_completion_time


# Example usage
if __name__ == "__main__":
    # Tasks and their processing times
    tasks = [0, 1, 2, 3, 4]
    task_processing_times = [3, 2, 4, 1, 3]

    # Precedence constraints between tasks
    precedence_constraints = {
        0: [1, 2],  # Task 0 must be completed before tasks 1 and 2
        1: [3],     # Task 1 must be completed before task 3
        2: [3, 4]   # Task 2 must be completed before tasks 3 and 4
    }

    task_assignment, total_completion_time = list_scheduling(tasks, precedence_constraints, task_processing_times)

    print("Task Assignment:", task_assignment)
    print("Total Completion Time:", total_completion_time)
