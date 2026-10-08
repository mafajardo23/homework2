import csv

data_pairs = []

with open("dataset1.csv") as data_file:
    read = csv.reader(data_file)
    next(read)              # First line skip 
    for row in read:
        x = float(row[0])
        y = float(row[1])
        data_pairs.append((x,y))

