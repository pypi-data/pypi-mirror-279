#Optimum Communication Spanning Tree

import random

def generate_population(n, edges, population_size):
    # generate a random population of solutions
    population = []
    for _ in range(population_size):
        # generate a random solution
        solution = [random.randint(0, 1) for _ in range(len(edges))]
        population.append(solution)
    return population

def evaluate_solution(solution, edges):
    # evaluate the fitness of a solution
    fitness = 0
    for i, edge in enumerate(edges):
        if solution[i] == 1:
            fitness += edge[2]
    return fitness

def genetic_algorithm(n, edges, population_size, generations):
    population = generate_population(n, edges, population_size)
    for generation in range(generations):
        # evaluate the fitness of each solution
        fitness = [evaluate_solution(s, edges) for s in population]

        # select the best solutions for breeding
        parents = [population[i] for i in range(population_size) if fitness[i] == max(fitness)]

        # breed the solutions to generate the next generation
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

    # evaluate the fitness of the final population
    fitness = [evaluate_solution(s, edges) for s in population]
    best_solution = population[fitness.index(max(fitness))]

    # extract the edges from the best solution
    tree = []
    for i, edge in enumerate(edges):
        if best_solution[i] == 1:
            tree.append(edge)
    return tree
