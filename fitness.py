import csv
from treeInstance import grow, traversal
import random 

data_pairs = []
fit_pairs = []
population = []


#Reading the data and storing it in a list of tuples
with open("dataset1.csv") as data_file:
    read = csv.reader(data_file)
    next(read)              # First line skip 
    for row in read:
        x = float(row[0])
        y = float(row[1])
        data_pairs.append((x,y))

#Creating the trees
for i in range(10):
    population.append(grow(0, 3))

for tree in population:
    total = 0

    for x, y in data_pairs:
        test_output = traversal(tree, x)
        diff = y - test_output
        total += diff ** 2

    fitness_value = total / len(data_pairs)

    fit_pairs.append((fitness_value, tree))



for i in range(len(population)):
    print(fit_pairs[i][0], fit_pairs[i][1])

TOURNAMENT_SIZE = 3

def tournament_parent_select(fit_pairs, num_parents):
    parents = []

    for tour_size in range(num_parents):
        sample = []

        for sample_size in range(TOURNAMENT_SIZE):
            sample.append(random.choice(fit_pairs))

        sample.sort(key=lambda pair: pair[0])
        parents.append(sample[0][1]) #adding the tree

    return parents
