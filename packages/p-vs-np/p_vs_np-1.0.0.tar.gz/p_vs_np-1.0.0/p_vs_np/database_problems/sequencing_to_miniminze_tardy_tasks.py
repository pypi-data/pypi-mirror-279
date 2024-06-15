#Sequencing to Miniminze Tardy Tasks








# Example usage
    # List of jobs [job_id, release_time, deadline, processing_time]



if __name__ == '__main__':
    def job_scheduling_tardiness(jobs):
        sorted_jobs = sorted(jobs, key=lambda x: x[2])  # Sort jobs by deadline (ascending order)
        schedule = []
        current_time = 0
        total_tardiness = 0
        for job in sorted_jobs:
            release_time = job[1]
            deadline = job[2]
            processing_time = job[3]
            if current_time < release_time:
                current_time = release_time
            if current_time <= deadline:
                schedule.append(job[0])
                current_time += processing_time
            else:
                tardiness = current_time - deadline
                total_tardiness += tardiness
        return schedule, total_tardiness
    if __name__ == "__main__":
        jobs = [
            [1, 0, 3, 2],
            [2, 2, 5, 1],
            [3, 1, 4, 3],
            [4, 4, 6, 2],
            [5, 3, 8, 4]
        ]
        schedule, total_tardiness = job_scheduling_tardiness(jobs)
        print("Job schedule:", schedule)
        print("Total tardiness:", total_tardiness)
