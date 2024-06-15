#Sequencing to minimize weighted tardiness






# Example usage
    # List of jobs [weight, processing_time, due_date]



if __name__ == '__main__':
    def job_scheduling_weighted_tardiness(jobs):
        sorted_jobs = sorted(jobs, key=lambda x: x[2])  # Sort jobs by due dates (ascending order)
        n = len(sorted_jobs)
        completion_time = 0
        weighted_tardiness = 0
        for i in range(n):
            weight = sorted_jobs[i][0]
            processing_time = sorted_jobs[i][1]
            due_date = sorted_jobs[i][2]
            completion_time += processing_time
            tardiness = max(0, completion_time - due_date)
            weighted_tardiness += weight * tardiness
        return weighted_tardiness
    if __name__ == "__main__":
        jobs = [
            [4, 5, 8],
            [2, 3, 10],
            [1, 2, 4],
            [5, 4, 6],
            [3, 1, 7]
        ]
        min_weighted_tardiness = job_scheduling_weighted_tardiness(jobs)
        print("Minimum weighted tardiness:", min_weighted_tardiness)
