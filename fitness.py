import csv
from treeInstance import grow, traversal

data_pairs = []
fitness = []
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
for i in range(2):
    population.append(grow(0, 3))

for tree in population:
    total = 0

    for x, y in data_pairs:
        test_output = traversal(tree, x)
        diff = y - test_output
        total += diff 

    fitness_value = total / len(data_pairs)
    fitness.append(fitness_value)


#Showing each tree with its fitness score
for i in range(len(population)):
    print(fitness[i], population[i])