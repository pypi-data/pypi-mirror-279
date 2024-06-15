#Optimum Communication Spanning Tree


    # generate a random population of solutions
        # generate a random solution

    # evaluate the fitness of a solution

        # evaluate the fitness of each solution

        # select the best solutions for breeding

        # breed the solutions to generate the next generation

    # evaluate the fitness of the final population

    # extract the edges from the best solution

if __name__ == '__main__':
    import random
    def generate_population(n, edges, population_size):
        population = []
        for _ in range(population_size):
            solution = [random.randint(0, 1) for _ in range(len(edges))]
            population.append(solution)
        return population
    def evaluate_solution(solution, edges):
        fitness = 0
        for i, edge in enumerate(edges):
            if solution[i] == 1:
                fitness += edge[2]
        return fitness
    def genetic_algorithm(n, edges, population_size, generations):
        population = generate_population(n, edges, population_size)
        for generation in range(generations):
            fitness = [evaluate_solution(s, edges) for s in population]
            parents = [population[i] for i in range(population_size) if fitness[i] == max(fitness)]
            children = []
            while len(children) < population_size:
                parent1 = random.choice(parents)
                parent2 = random.choice(parents)
                child = []
                for i in range(len(edges)):
                    if random.random() < 0.5:
                        child.append(parent1[i])
                    else:
                        child.append(parent2[i])
                children.append(child)
            population = children
        fitness = [evaluate_solution(s, edges) for s in population]
        best_solution = population[fitness.index(max(fitness))]
        tree = []
        for i, edge in enumerate(edges):
            if best_solution[i] == 1:
                tree.append(edge)
        return tree
