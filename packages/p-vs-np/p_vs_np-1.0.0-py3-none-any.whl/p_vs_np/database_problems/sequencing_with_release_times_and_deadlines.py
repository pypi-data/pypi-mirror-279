#Sequencing with release times and deadlines








# Example usage
    # List of jobs [job_id, release_time, deadline]


if __name__ == '__main__':
    def job_scheduling(jobs):
        sorted_jobs = sorted(jobs, key=lambda x: x[2])  # Sort jobs by deadline (ascending order)
        schedule = []
        current_time = 0
        for job in sorted_jobs:
            release_time = job[1]
            deadline = job[2]
            if current_time < release_time:
                current_time = release_time
            if current_time <= deadline:
                schedule.append(job[0])
                current_time += 1
        return schedule
    if __name__ == "__main__":
        jobs = [
            [1, 0, 3],
            [2, 2, 5],
            [3, 1, 4],
            [4, 4, 6],
            [5, 3, 8]
        ]
        schedule = job_scheduling(jobs)
        print("Job schedule:", schedule)
