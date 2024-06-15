#Sequencing to Minimize Tardy Task Weight


def job_scheduling_tardiness_weighted(jobs):
    sorted_jobs = sorted(jobs, key=lambda x: x[2])  # Sort jobs by deadline (ascending order)
    n = len(sorted_jobs)
    dp = [0] * (n + 1)  # Dynamic programming table

    for i in range(1, n + 1):
        weight = sorted_jobs[i - 1][0]
        deadline = sorted_jobs[i - 1][2]
        processing_time = sorted_jobs[i - 1][3]
        dp[i] = max(weight + dp[i - 1], dp[i - 1]) if i == 1 else max(weight + dp[i - 1], dp[i - 2] + processing_time)

    return dp[n]


# Example usage
if __name__ == "__main__":
    # List of jobs [weight, release_time, deadline, processing_time]
    jobs = [
        [4, 1, 3, 2],
        [2, 2, 5, 1],
        [1, 0, 4, 3],
        [5, 3, 8, 4],
        [3, 4, 6, 2]
    ]

    min_tardy_task_weight = job_scheduling_tardiness_weighted(jobs)
    print("Minimum tardy task weight:", min_tardy_task_weight)
