#Multiprocessor



    # Sort tasks in descending order of processing time

    # Assign tasks to processors using List Scheduling





# Example usage
    # Number of processors and tasks

    # Processing times for each task




if __name__ == '__main__':
    Processing
    def list_scheduling(num_processors, task_processing_times):
        num_tasks = len(task_processing_times)
        task_assignment = [None] * num_tasks
        processor_loads = [0] * num_processors
        sorted_tasks = sorted(range(num_tasks), key=lambda x: task_processing_times[x], reverse=True)
        for task in sorted_tasks:
            min_load = min(processor_loads)
            min_load_processor = processor_loads.index(min_load)
            task_assignment[task] = min_load_processor
            processor_loads[min_load_processor] += task_processing_times[task]
        total_completion_time = max(processor_loads)
        return task_assignment, total_completion_time
    if __name__ == "__main__":
        num_processors = 3
        num_tasks = 5
        task_processing_times = [3, 2, 4, 1, 3]
        task_assignment, total_completion_time = list_scheduling(num_processors, task_processing_times)
        print("Task Assignment:", task_assignment)
        print("Total Completion Time:", total_completion_time)
