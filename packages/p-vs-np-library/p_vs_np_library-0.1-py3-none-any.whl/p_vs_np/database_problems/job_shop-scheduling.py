#Job Shop-Scheduling

def list_scheduling(jobs, machines):
    num_jobs = len(jobs)
    num_machines = len(machines)

    schedule = [[] for _ in range(num_machines)]
    completion_times = [0] * num_machines

    remaining_operations = [len(job) for job in jobs]

    while sum(remaining_operations) > 0:
        for job_id, job in enumerate(jobs):
            if remaining_operations[job_id] > 0:
                next_operation = job[len(job) - remaining_operations[job_id]]
                machine_id = next_operation[0]
                processing_time = next_operation[1]

                start_time = max(completion_times[machine_id], completion_times[1 - machine_id])
                completion_time = start_time + processing_time

                schedule[machine_id].append((job_id, start_time, completion_time))
                completion_times[machine_id] = completion_time

                remaining_operations[job_id] -= 1

    makespan = max(completion_times)

    return schedule, makespan


# Example usage
if __name__ == "__main__":
    # Jobs, each represented as a list of operations, where each operation is (machine_id, processing_time)
    jobs = [
        [(0, 3), (1, 2), (2, 4)],  # Job 0: Operations [(Machine 0, 3), (Machine 1, 2), (Machine 2, 4)]
        [(1, 1), (2, 3), (0, 2)],  # Job 1: Operations [(Machine 1, 1), (Machine 2, 3), (Machine 0, 2)]
        [(2, 5), (0, 1), (1, 4)]   # Job 2: Operations [(Machine 2, 5), (Machine 0, 1), (Machine 1, 4)]
    ]

    machines = [0, 1, 2]  # List of machine IDs

    schedule, makespan = list_scheduling(jobs, machines)

    print("Job Schedule:")
    for machine_id, tasks in enumerate(schedule):
        print(f"Machine {machine_id}:")
        for task in tasks:
            job_id = task[0]
            start_time = task[1]
            completion_time = task[2]
            print(f"Job {job_id}: Start Time = {start_time}, Completion Time = {completion_time}")
        print()

    print("Makespan:", makespan)
