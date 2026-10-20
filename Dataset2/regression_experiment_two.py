import csv
import math

import random 
import os

from Dataset2.treeInstance_two import grow, traversal
from Dataset2.genetic_program_two import crossover, mutate, reproduction, get_tree_paths

random.seed(int(os.environ.get("SLURM_ARRAY_TASK_ID", 0)))


#Configurations
data_pairs = []
population = []
TOURNAMENT_SIZE = 3
POPULATION_SIZE = 200
TARGET = 0.01
MAX_ITERATIONS = 50
PLATEAU = 15
TEST_PERCENT = 0.20 


#Reading the data and storing it in a list as pairs (x, y)
with open("Dataset2/dataset2.csv") as data_file:
    read = csv.reader(data_file)
    next(read)              # First line skip 
    for row in read:
        x1 = float(row[0]) / 1000000
        x2 = float(row[1]) / 1000000
        x3 = float(row[2])
        y = float(row[3])
        if x3 < 0.05:        # skip rows where x3 is basically 0 because they will increase so much
            continue
        data_pairs.append(((x1, x2, x3), y))

test_data_size = int(len(data_pairs) * TEST_PERCENT)

test_data = data_pairs[:test_data_size]     # first 20% test set for later
train_data = data_pairs[test_data_size:]

"""
    Calculate fitness helper. Function that calculates how wrong the tree is.
"""
def mean_squared_error(tree, data_pairs):
    total = 0
    for x, y in data_pairs:
        diff = (y - traversal(tree, x)) / (y + 1)
        total += diff ** 2
        if not math.isfinite(total): #if we get a total thats not a real number i.e. inf or nan
            total = float('inf')  #then give that tree the worst score                 total = float('inf')  #then give that tree the worst score 
            break  #and stop checking it. i.e. no need to check other points because it already has a bad fitness score.

    return total / len(data_pairs)


def calculate_fitness(population, data_pairs):
    """
    Function that takes in the list of the tree population, the pairs for
    input and output and calculates the fitness measure for each tree in the
    population with MSE. Returns a list of pairs with the fitness value as first value
    and the tree as a second value.
    """

    fit_pairs = []
    for tree in population:
        fitness_value = mean_squared_error(tree, data_pairs)   
        fit_pairs.append((fitness_value, tree))
    return fit_pairs


def tournament_parent_select(fit_pairs, num_parents):
    """
    Function that does the tournament selection method to return a set amount
    of parents. Randomly selects choices from our generated trees, sorts them
    from least to greatest error and appends the best one out of those sample size trees.
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
    fit_pairs = calculate_fitness(population, train_data)    
    fit_pairs.sort(key=lambda pair: pair[0])
    best_tree = fit_pairs[0]

    # Check: if the best tree has the same fitness as last generation's best, keep the smaller tree
    if len(best_per_generation) > 0:
        prev_tree = best_per_generation[-1]
        if round(best_tree[0], 4) == round(prev_tree[0], 4):
            if len(get_tree_paths(prev_tree[1])) < len(get_tree_paths(best_tree[1])):
                best_tree = prev_tree

    best_per_generation.append(best_tree)   # adds the best pair to the list
    scores.append(best_tree[0])    # adds just the score
    print(generation, best_tree[0], best_tree[1], "unique:", len(set(population)))  # score, tree, and how many different trees

    #if the best tree reached the target, done
    if best_tree[0] < TARGET:                        
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


best_overall = best_per_generation[-1]

print(generation, best_tree[0], best_tree[1], "unique:", len(set(population)))  # score, tree, and how many different trees


best_tree =  best_overall[1]
best_train = mean_squared_error(best_tree, train_data)
best_test = mean_squared_error(best_tree, test_data)
#Error check 
print("Train error", best_train, "Test error", best_test)

limit = best_train * 1.5

if best_test <= limit:
    print("Not overfitting. Test set is relatively similar to best fit line of trained data")
else:
    print("Overfitting. test error is way bigger than the fit line, meaning its going directly to the points rather than the line of best fit  ")