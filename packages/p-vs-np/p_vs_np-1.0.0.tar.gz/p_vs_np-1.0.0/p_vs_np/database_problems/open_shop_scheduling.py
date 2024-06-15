#Open Shop Scheduling







# Example usage
    # Jobs and their processing times on each machine

    # Machines with their IDs




if __name__ == '__main__':
    def list_scheduling(jobs, machines):
        num_jobs = len(jobs)
        num_machines = len(machines)
        schedule = [[] for _ in range(num_machines)]
        completion_times = [0] * num_machines
        for job in jobs:
            for machine in machines:
                machine_id = machine[0]
                processing_time = job[machine_id]
                start_time = completion_times[machine_id]
                completion_time = start_time + processing_time
                schedule[machine_id].append((job[0], start_time, completion_time))
                completion_times[machine_id] = completion_time
        makespan = max(completion_times)
        return schedule, makespan
    if __name__ == "__main__":
        jobs = [
            (0, [2, 3, 1]),  # Job 0: Processing times on machines [2, 3, 1]
            (1, [4, 1, 2]),  # Job 1: Processing times on machines [4, 1, 2]
            (2, [3, 2, 1])   # Job 2: Processing times on machines [3, 2, 1]
        ]
        machines = [
            (0, "Machine A"),
            (1, "Machine B"),
            (2, "Machine C")
        ]
        schedule, makespan = list_scheduling(jobs, machines)
        print("Job Schedule:")
        for machine_id, tasks in enumerate(schedule):
            machine_name = machines[machine_id][1]
            print(f"{machine_name}:")
            for task in tasks:
                print(f"Job {task[0]}: Start Time = {task[1]}, Completion Time = {task[2]}")
            print()
        print("Makespan:", makespan)
