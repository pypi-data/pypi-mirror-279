#Scheduling to minimize weighted completion time

def spt_scheduling(tasks):
    tasks.sort(key=lambda x: x[1])  # Sort tasks based on processing times
    schedule = []
    current_time = 0
    weighted_completion_time = 0

    for task in tasks:
        task_id, processing_time, weight = task
        completion_time = current_time + processing_time
        schedule.append((task_id, current_time, completion_time))
        weighted_completion_time += weight * completion_time
        current_time = completion_time

    return schedule, weighted_completion_time


# Example usage
if __name__ == "__main__":
    # Tasks and their processing times and weights
    tasks = [
        (0, 4, 2),  # Task 0 has processing time 4 and weight 2
        (1, 5, 3),  # Task 1 has processing time 5 and weight 3
        (2, 3, 1),  # Task 2 has processing time 3 and weight 1
        (3, 2, 4)   # Task 3 has processing time 2 and weight 4
    ]

    schedule, weighted_completion_time = spt_scheduling(tasks)

    print("Task Schedule:")
    for task in schedule:
        print(f"Task {task[0]}: Start Time = {task[1]}, Completion Time = {task[2]}")

    print("Weighted Completion Time:", weighted_completion_time)


