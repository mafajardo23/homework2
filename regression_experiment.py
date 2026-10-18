import csv
import math
from treeInstance import grow, traversal
import random 
from genetic_program import crossover, mutate, reproduction
import os

random.seed(int(os.environ.get("SLURM_ARRAY_TASK_ID", 0)))


#Configurations
data_pairs = []
population = []
TOURNAMENT_SIZE = 3
POPULATION_SIZE = 200
TARGET = 0.01
MAX_ITERATIONS = 50
PLATEAU = 20


#Reading the data and storing it in a list as pairs (x, y)
with open("dataset1.csv") as data_file:
    read = csv.reader(data_file)
    next(read)              # First line skip 
    for row in read:
        x = float(row[0])
        y = float(row[1])
        data_pairs.append((x,y))



data_pairs = data_pairs[:2000]    

#Function 
def calculate_fitness(population, data_pairs):
    """
    Function that takes in the list of the tree population, the pairs for
    input and output and calculates the fitness measure for each tree in the
    population. Returns a list of pairs with the fitness value as first value
    and the tree as a second value. 
    """
    fit_pairs = []

    for tree in population:
        total = 0

        for x, y in data_pairs:
            test_output = traversal(tree, x)
            diff = y - test_output
            total += diff * diff     #diff ** 2

            if not math.isfinite(total): #if we get a total thats not a real number i.e. inf or nan
                total = float('inf')  #then give that tree the worst score 
                break  #and stop checking it. i.e. no need to check other points because it already has a bad fitness score.

        fitness_value = total / len(data_pairs)
        fit_pairs.append((fitness_value, tree))


    return fit_pairs


def tournament_parent_select(fit_pairs, num_parents):
    """
    Function that does the tournament selection method to return a set amount 
    of parents. Randomly selects choices from our generated trees, sorts them
    from greatest to least and appends the best one out of those sample size trees. 
    returns the parent list. This makes sure that our selection is not greedy,  
    individuals that are known to be inferior will be selected to a certain degree. 
    """
    parents = []

    for tour_size in range(num_parents):
        sample = []

        for sample_size in range(TOURNAMENT_SIZE):
            sample.append(random.choice(fit_pairs))

        sample.sort(key=lambda pair: pair[0])
        parents.append(sample[0][1]) #adding the tree

    return parents


def make_new_population(fit_pairs, num_parents):
    """
    Function that organizes the logistics for the GP. It creates a new population,
    forces the best one to be in the population, and calls the parents function. 
    With that new list of parents, organizes them to be called by the different GP
    methods, and returns a new list with all the trees altered by GP. 
    """
    new_population = []
    #always have the best tree make it
    elite = min(fit_pairs, key=lambda pair: pair[0])
    new_population.append(elite[1])

    parents = tournament_parent_select(fit_pairs, num_parents)

    # split 90% crossover, 8% reproduction, 2% mutation
    num_cross = int(num_parents * 0.90)
    if num_cross % 2 == 1:                         
        num_cross -= 1

    num_mutate = max(1, round(num_parents * 0.02))  # at least 1
    num_reprod = num_parents - num_cross - num_mutate - 1 #elite   

    #assigning parents
    cross_parents = parents[:num_cross]
    repro_parents = parents[num_cross : num_cross + num_reprod]
    mut_parents   = parents[num_cross + num_reprod : num_cross + num_reprod + num_mutate] #mutate starts where reproduction ended, and takes num_mutate parents


    #crossover (90%)
    for i in range(0, num_cross, 2):
        child1, child2 = crossover(cross_parents[i], cross_parents[i + 1])
        new_population.append(child1)
        new_population.append(child2)

    #reproduction (8%)
    for tree in repro_parents:
        new_population.append(reproduction(tree))

    #mutation (2%)
    for tree in mut_parents:
        new_population.append(mutate(tree))

    return new_population


#CREATING THE POPULATION
for i in range(POPULATION_SIZE):
    population.append(grow(0, 3))

best_per_generation = []
scores = []
generation = 0

#MAIN LOOP
while True:
    #calculate
    fit_pairs = calculate_fitness(population, data_pairs)
    fit_pairs.sort(key=lambda pair: pair[0])    

    best_per_generation.append(fit_pairs[0]) # adds the best pair to the list
    scores.append(fit_pairs[0][0])  # adds just the score
    print(generation, fit_pairs[0][0], fit_pairs[0][1])   # score and tree

    #if the best tree reached the target, done
    if fit_pairs[0][0] < TARGET:
        print("Found it!")
        break

    if len(scores) > PLATEAU: 
        old = scores[generation - PLATEAU] # score from PLATEAU gens ago
        new = scores[generation]    # score now
        if old - new < 0.01:   # check if it has barely improved
            print("Plateau reached")
            break

    if generation >= MAX_ITERATIONS:
        print("Max iterations reached")
        break

    population = make_new_population(fit_pairs, POPULATION_SIZE)
    generation += 1

best_per_generation.sort(key=lambda pair: pair[0])
best_overall = best_per_generation[0]
print("Best overall:", best_overall[0], best_overall[1])






    