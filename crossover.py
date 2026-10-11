"""
Crossover logic:
- Pick two trees.
- For each tree, get all the paths in the tree and store them. 
- Pick a path from each tree. 
- Swap the paths from the two trees.

Use helper functions to pick the trees, and get the paths. 

NB: Remember to store the new functions tht 
"""

## Step 1: Pick two random parent trees from the pool of candidate functions:
parent1 = random.choice(candidate_functions)
parent2 = random.choice(candidate_functions)


## Step 2: Determine the paths of the trees (think of them as indices)
def get_tree_paths(tree, current_path = [], paths = None):
    if paths is None: 
        paths = []

    paths.append(current_path)

    if isinstance(tree, tuple):
        tree = operator, left, right
        get_tree_paths(left, current_path + [1], paths)
        get_tree_paths(right, current_path + [2], paths)

    return paths



## Call paths for parent 1:
paths_parent1 = get_tree_paths(parent1)

# Pick a random path to crossover
path1 = random.choice(paths_parent1)


## Call paths for parent 2:
paths_parent2 = get_tree_paths(parent2)

# Pick a random path to crossover
path2 = random.choice(paths_parent2)


## Swap the subtrees at the paths from the two trees

# First, retrieve those subtrees at a certain path;
def retrieve_subtree(tree, path):
    for i in path: 
        node = tree[i]
    return node

subtree1 = retrieve_subtree(parent1, path1)
subtree2 = retrieve_subtree(parent2, path2)


# Second, then swap the subtrees
def swap_subtrees(tree, path, new_subtree):

    #we want to edit the tree but its a tuple, so change it to a list
    node = to_list(tree)

    for i in path[:-1]:
        node = node[i]

    #Then set the subtree at that spot equal to the new piece: 
    node[path[-1]] = new_subtree


def crossover(parent1, parent2):
    ## Call paths for parent 1:
    paths_parent1 = get_tree_paths(parent1)

    # Pick a random path to crossover
    path1 = random.choice(paths_parent1)


    ## Call paths for parent 2:
    paths_parent2 = get_tree_paths(parent2)

    # Pick a random path to crossover
    path2 = random.choice(paths_parent2)



