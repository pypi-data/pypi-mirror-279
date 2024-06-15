#Sequencing to minimize weighted Completion Time


def job_scheduling_completion_time(jobs):
    sorted_jobs = sorted(jobs, key=lambda x: x[1])  # Sort jobs by processing time (ascending order)
    n = len(sorted_jobs)
    completion_time = 0
    weighted_completion_time = 0

    for i in range(n):
        weight = sorted_jobs[i][0]
        processing_time = sorted_jobs[i][1]
        completion_time += processing_time
        weighted_completion_time += weight * completion_time

    return weighted_completion_time


# Example usage
if __name__ == "__main__":
    # List of jobs [weight, processing_time]
    jobs = [
        [4, 5],
        [2, 3],
        [1, 2],
        [5, 4],
        [3, 1]
    ]

    min_weighted_completion_time = job_scheduling_completion_time(jobs)
    print("Minimum weighted completion time:", min_weighted_completion_time)

