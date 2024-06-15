#Sequencing with deadlines and set up times



    # Initialize the machines

    # Assign jobs to the machines based on the set-up times

    # Reverse the order of jobs on machine2

    # Merge the schedules of the two machines

    # Append the remaining jobs from machine1 or machine2

    # Compute the completion times and total completion time




# Example usage
    # List of jobs [processing_time, set_up_time]



if __name__ == '__main__':
    def job_scheduling_deadlines_setup_times(jobs):
        n = len(jobs)
        sorted_jobs = sorted(jobs, key=lambda x: x[1])  # Sort jobs by set-up times (ascending order)
        schedule = []
        machine1 = []
        machine2 = []
        for i in range(n):
            if sorted_jobs[i][0] <= sorted_jobs[i][1]:
                machine1.append(sorted_jobs[i][0])
            else:
                machine2.append(sorted_jobs[i][0])
        machine2.reverse()
        while machine1 and machine2:
            if machine1[0] <= machine2[0]:
                schedule.append(machine1.pop(0))
            else:
                schedule.append(machine2.pop(0))
        schedule.extend(machine1)
        schedule.extend(machine2)
        completion_times = [0]
        total_completion_time = 0
        for job in schedule:
            completion_time = completion_times[-1] + job
            completion_times.append(completion_time)
            total_completion_time += completion_time
        return schedule, total_completion_time
    if __name__ == "__main__":
        jobs = [
            [3, 2],
            [4, 1],
            [2, 3],
            [5, 2],
            [1, 4]
        ]
        schedule, min_completion_time = job_scheduling_deadlines_setup_times(jobs)
        print("Schedule:", schedule)
        print("Total completion time:", min_completion_time)
