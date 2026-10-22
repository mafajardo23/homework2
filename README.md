# Symbolic Regression with Genetic Programming

CSC 370, Homework 2 (Fall 2026)
Maria and Tania

This project uses genetic programming (GP) to find the hidden function behind two datasets, using only input and output data.

- Dataset 1: one input `x`, output `f(x)`
- Dataset 2: three inputs `x1`, `x2`, `x3`, output `y`

## Requirements

- Python 3
- No external packages (only the standard library: `csv`, `math`, `random`, `os`)

## Project structure

```
Dataset1/
    dataset1.csv               # the data (25,000 rows)
    treeInstance.py            # building blocks, random tree generation, tree evaluation
    genetic_program.py         # crossover, mutation, reproduction, depth limit
    regression_experiment.py   # main GP loop: fitness, selection, stopping, train/test check

Dataset2/
    dataset2.csv
    treeInstance_two.py
    genetic_program_two.py
    regression_experiment_two.py
```

## How to run

Run from the repository root, so the `Dataset1/...` and `Dataset2/...` imports and file
