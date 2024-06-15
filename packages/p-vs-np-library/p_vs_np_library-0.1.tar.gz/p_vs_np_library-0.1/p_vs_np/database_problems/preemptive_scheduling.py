#Preemptive Scheduling

def list_scheduling(tasks):
    tasks.sort(key=lambda x: x[0])  # Sort tasks based on release times
    schedule = []
    current_time = 0

    for task in tasks:
        task_id, release_time, duration, deadline = task
        if current_time < release_time:
            current_time = release_time
        completion_time = current_time + duration
        schedule.append((task_id, current_time, completion_time))
        current_time = completion_time

    return schedule


# Example usage
if __name__ == "__main__":
    # Tasks and their release times, durations, and deadlines
    tasks = [
        (0, 0, 4, 10),  # Task 0 has release time 0, duration 4, and deadline 10
        (1, 2, 5, 12),  # Task 1 has release time 2, duration 5, and deadline 12
        (2, 1, 3, 6),   # Task 2 has release time 1, duration 3, and deadline 6
        (3, 4, 2, 8)    # Task 3 has release time 4, duration 2, and deadline 8
    ]

    schedule = list_scheduling(tasks)

    print("Task Schedule:")
    for task in schedule:
        print(f"Task {task[0]}: Start Time = {task[1]}, Completion Time = {task[2]}")
