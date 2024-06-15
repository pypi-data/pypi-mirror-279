#Sequencing to minimize maximum cumulative cost




























# Example usage
    # Number of jobs and machines

    # Processing times for each job on each machine

    # Genetic Algorithm parameters



if __name__ == '__main__':
    import random
    def initialize_population(num_jobs, num_machines, population_size):
        population = []
        for _ in range(population_size):
            chromosome = [random.sample(range(num_machines), num_machines) for _ in range(num_jobs)]
            population.append(chromosome)
        return population
    def calculate_fitness(chromosome, job_processing_times):
        machine_completion_times = [0] * len(chromosome[0])
        job_completion_times = []
        for job in chromosome:
            job_completion_time = []
            for machine, processing_time in zip(job, job_processing_times):
                completion_time = max(machine_completion_times[machine], sum(machine_completion_times[:machine + 1]))
                machine_completion_times[machine] = completion_time + processing_time
                job_completion_time.append(completion_time)
            job_completion_times.append(job_completion_time)
        return max(machine_completion_times), job_completion_times
    def crossover(parent1, parent2):
        num_jobs = len(parent1)
        num_machines = len(parent1[0])
        cutoff = random.randint(1, num_jobs - 1)
        child1 = parent1[:cutoff] + parent2[cutoff:]
        child2 = parent2[:cutoff] + parent1[cutoff:]
        return child1, child2
    def mutate(chromosome, mutation_rate):
        num_jobs = len(chromosome)
        num_machines = len(chromosome[0])
        for i in range(num_jobs):
            for j in range(num_machines):
                if random.random() < mutation_rate:
                    chromosome[i][j] = random.randint(0, num_machines - 1)
        return chromosome
    def genetic_algorithm(num_jobs, num_machines, job_processing_times, population_size, generations, mutation_rate):
        population = initialize_population(num_jobs, num_machines, population_size)
        for _ in range(generations):
            new_population = []
            for _ in range(population_size // 2):
                parent1 = random.choice(population)
                parent2 = random.choice(population)
                child1, child2 = crossover(parent1, parent2)
                child1 = mutate(child1, mutation_rate)
                child2 = mutate(child2, mutation_rate)
                new_population.extend([child1, child2])
            population = new_population
        best_chromosome = max(population, key=lambda x: calculate_fitness(x, job_processing_times)[0])
        max_cumulative_cost, job_completion_times = calculate_fitness(best_chromosome, job_processing_times)
        return best_chromosome, max_cumulative_cost, job_completion_times
    if __name__ == "__main__":
        num_jobs = 5
        num_machines = 3
        job_processing_times = [
            [2, 4, 3],
            [3, 1, 2],
            [4, 2, 3],
            [2, 3, 2],
            [1, 4, 3]
        ]
        population_size = 50
        generations = 100
        mutation_rate = 0.1
        best_chromosome, max_cumulative_cost, job_completion_times = genetic_algorithm(
            num_jobs, num_machines, job_processing_times, population_size, generations, mutation_rate
        )
        print("Best Chromosome:", best_chromosome)
        print("Max Cumulative Cost:", max_cumulative_cost)
        print("Job Completion Times:", job_completion_times)
