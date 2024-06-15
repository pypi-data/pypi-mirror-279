#Multiprocessor
Processing


def list_scheduling(num_processors, task_processing_times):
    num_tasks = len(task_processing_times)
    task_assignment = [None] * num_tasks
    processor_loads = [0] * num_processors

    # Sort tasks in descending order of processing time
    sorted_tasks = sorted(range(num_tasks), key=lambda x: task_processing_times[x], reverse=True)

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
    # Number of processors and tasks
    num_processors = 3
    num_tasks = 5

    # Processing times for each task
    task_processing_times = [3, 2, 4, 1, 3]

    task_assignment, total_completion_time = list_scheduling(num_processors, task_processing_times)

    print("Task Assignment:", task_assignment)
    print("Total Completion Time:", total_completion_time)

