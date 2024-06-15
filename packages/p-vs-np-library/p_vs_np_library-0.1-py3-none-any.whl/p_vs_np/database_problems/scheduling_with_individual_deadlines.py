#Scheduling with Individual Deadlines

def edf_scheduling(tasks):
    tasks.sort(key=lambda x: x[1])  # Sort tasks based on deadlines
    schedule = []
    current_time = 0
    max_lateness = 0

    for task in tasks:
        task_id, duration, deadline = task
        completion_time = current_time + duration
        lateness = completion_time - deadline

        schedule.append((task_id, current_time, completion_time))
        current_time = completion_time
        max_lateness = max(max_lateness, lateness)

    return schedule, max_lateness


# Example usage
if __name__ == "__main__":
    # Tasks and their durations and deadlines
    tasks = [
        (0, 3, 6),  # Task 0 has duration 3 and deadline 6
        (1, 2, 4),  # Task 1 has duration 2 and deadline 4
        (2, 4, 7),  # Task 2 has duration 4 and deadline 7
        (3, 1, 3)   # Task 3 has duration 1 and deadline 3
    ]

    schedule, max_lateness = edf_scheduling(tasks)

    print("Task Schedule:")
    for task in schedule:
        print(f"Task {task[0]}: Start Time = {task[1]}, Completion Time = {task[2]}")
    print("Max Lateness:", max_lateness)
