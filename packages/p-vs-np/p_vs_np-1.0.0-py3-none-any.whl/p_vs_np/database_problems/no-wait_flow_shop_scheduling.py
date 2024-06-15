#No-wait flow shop scheduling

def johnsons_algorithm(jobs):
    num_jobs = len(jobs)
    num_machines = len(jobs[0])

    schedule = [[] for _ in range(num_machines)]
    completion_times = [0] * num_machines

    sorted_jobs = sorted(jobs, key=lambda job: min(job[0], job[1], job[2]))

    for job in sorted_jobs:
        processing_time_machine1, processing_time_machine2, processing_time_machine3 = job

        if (
            completion_times[0] + processing_time_machine1 <= completion_times[1]
            and completion_times[0] + processing_time_machine1 <= completion_times[2]
        ):
            machine_id = 0
        elif (
            completion_times[1] + processing_time_machine2 <= completion_times[0]
            and completion_times[1] + processing_time_machine2 <= completion_times[2]
        ):
            machine_id = 1
        else:
            machine_id = 2

        start_time = completion_times[machine_id]
        completion_time = start_time + job[machine_id]
        schedule[machine_id].append((job, start_time, completion_time))
        completion_times[machine_id] = completion_time

    makespan = max(completion_times)

    return schedule, makespan


# Example usage
if __name__ == "__main__":
    # Jobs and their processing times on each machine
    jobs = [
        (2, 3, 4),  # Job 0: Processing times on machines [2, 3, 4]
        (4, 1, 2),  # Job 1: Processing times on machines [4, 1, 2]
        (3, 2, 5)   # Job 2: Processing times on machines [3, 2, 5]
    ]

    schedule, makespan = johnsons_algorithm(jobs)

    print("Job Schedule:")
    for machine_id, tasks in enumerate(schedule):
        print(f"Machine {machine_id + 1}:")
        for task in tasks:
            job = task[0]
            start_time = task[1]
            completion_time = task[2]
            print(f"Job {job}: Start Time = {start_time}, Completion Time = {completion_time}")
        print()

    print("Makespan:", makespan)
