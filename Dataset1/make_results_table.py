import csv 
import glob

rows = []

#Read the single rows from each run
for filename in glob.glob("results/run_*.csv"): 
    with open(filename) as f:
         reader = csv.reader(f)
         next(reader)
         rows.append(next(reader))


#arrange the runs in order:
rows.sort(key=lambda row: int(row[0]))

#Print table as a csv
with open("all_runs.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["run", "formula", "train_mse", "test_mse", "train_test_diff", "full_mse", "unique", "stop_reason"])
    writer.writerows(rows)

print("Saved", len(rows), "runs to all_runs.csv")#check how many runs were saved to see if its correctly saving the right amount of runs. 




"""
print("|run     | formula                        | train_mse       | test_mse        | full_mse          | unique     | stop_reason        |")
for row in rows: 
    print(" | ".join(row))
"""
            