import csv

inp = []
out = []

with open("dataset1.csv") as data_file:
    read = csv.reader(data_file)
    next(read)              # First line skip 
    for row in read:
        x = float(row[0])
        y = float(row[1])
        inp.append(x)
        out.append(y)

print(len(inp))   # should be 25000