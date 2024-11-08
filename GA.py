from typing import Tuple 
import numpy as np
# you need to install this package `ioh`. Please see documentations here: 
# https://iohprofiler.github.io/IOHexp/ and
# https://pypi.org/project/ioh/
import ioh
import sys
from ioh import get_problem, logger, ProblemClass
#1111
budget = 5000

# To make your results reproducible (not required by the assignment), you could set the random seed by
# `np.random.seed(some integer, e.g., 42)`

def studentnumber1_studentnumber2_GA(problem: ioh.problem.PBO) -> None:
    # initial_pop = ... make sure you randomly create the first population
    # `problem.state.evaluations` counts the number of function evaluation automatically,
    # which is incremented by 1 whenever you call `problem(x)`.
    # You could also maintain a counter of function evaluations if you prefer.
    global budget
    global pop_size, mutation_rate,crossover_rate
    '''
    pop_size = 100
    tournament_k = 10
    mutation_rate = 0.02
    crossover_probability = 0.5'''
    tournament_k=10
    parent = []
    parent_f = []
    for i in range(pop_size):
        # Initialization
        #print(size=problem.meta_data.n_variables)
        parent.append(np.random.randint(2, size = problem.meta_data.n_variables))
        #parent.append(np.random.randint(2, size=problem.dimension))
        parent_f.append(problem(parent[i]))
        budget = budget - 1
    while problem.state.evaluations < budget:
        #seletion
        print(333)
        def mating_selection(parent, parent_f):
            total_fitness = sum(parent_f)
            section_pro = []
            for f in parent_f:
                selection_probability = f / total_fitness
                section_pro.append(selection_probability)
            # print(section_pro)
            cumulative_probabilities = []
            cumulative_sum = 0.0
            for prob in section_pro:
                cumulative_sum += prob
                cumulative_probabilities.append(cumulative_sum)
            # print(cumulative_probabilities)

            selected = []
            for _ in range(pop_size):
                r = np.random.random()
                for i, cum_prob in enumerate(cumulative_probabilities):
                    if r < cum_prob:
                        selected.append(parent[i])
                        break
            return selected
        offspring = mating_selection(parent, parent_f)
        #tournament_k choose the top fitness
        offspring_fit = [problem(individual) for individual in offspring]
        offspring_with_fitness = list(zip(offspring, offspring_fit))
        offspring_with_fitness.sort(key=lambda x: x[1], reverse=True)
        tournament_individuals = offspring_with_fitness[:tournament_k]
        best_individuals = [individual[0] for individual in tournament_individuals]
        #define crossover
        def crossover(p1, p2):
            offstring1 = p1.copy()
            offstring2 = p2.copy()
            for i in range(len(p1)):
                if np.random.random() < crossover_rate:
                    offstring1[i] = p2[i]
                    offstring2[i] = p1[i]
            return offstring1, offstring2

        #define mutation
        def mutation(p):
            for i in range(len(p)):
                if np.random.uniform(0, 1) < mutation_rate:
                    p[i] = 1 - p[i]
            return p
        #crossover and mutation
        new_offspring = []
        for i in range(0, len(best_individuals) - 1):
            for j in range(i + 1, len(best_individuals)):
                parent1 = best_individuals[i]
                parent2 = best_individuals[j]
                child1, child2 = crossover(parent1, parent2)
                child1 = mutation(child1)
                child2 = mutation(child2)
                new_offspring.append(child1)
                new_offspring.append(child2)

        #the optimal values
        new_offspring_f = []
        for child in new_offspring:
            fitness = problem(child)
            new_offspring_f.append(fitness)
            budget -= 1
        parent = new_offspring[:pop_size]
        parent_f = new_offspring_f[:pop_size]



def create_problem(dimension: int, fid: int) -> Tuple[ioh.problem.PBO, ioh.logger.Analyzer]:
    # Declaration of problems to be tested.
    problem = get_problem(fid, dimension=dimension, instance=1, problem_class=ProblemClass.PBO)
    # Create default logger compatible with IOHanalyzer
    # `root` indicates where the output files are stored.
    # `folder_name` is the name of the folder containing all output. You should compress the folder 'run' and upload it to IOHanalyzer.
    l = logger.Analyzer(
        root="data",  # the working directory in which a folder named `folder_name` (the next argument) will be created to store data
        folder_name="run",  # the folder name to which the raw performance data will be stored
        algorithm_name="genetic_algorithm",  # name of your algorithm
        algorithm_info="Practical assignment of the EA course",
    )
    # attach the logger to the problem
    problem.attach_logger(l)
    return problem, l


if __name__ == "__main__":
    # this how you run your algorithm with 20 repetitions/independent run
    # create the LABS problem and the data logger
    F18, _logger = create_problem(dimension=50, fid=18)
    for run in range(20):
        studentnumber1_studentnumber2_GA(F18)
        F18.reset() # it is necessary to reset the problem after each independent run
    _logger.close() # after all runs, it is necessary to close the logger to make sure all data are written to the folder

    # create the N-Queens problem and the data logger
    F23, _logger = create_problem(dimension=49, fid=23)
    for run in range(20): 
        studentnumber1_studentnumber2_GA(F23)
        F23.reset()
    _logger.close()