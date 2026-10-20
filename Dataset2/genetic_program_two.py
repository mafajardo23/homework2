"""
This file contains both the crossover, mutation, and reproduction functions

Crossover logic:
- Pick two trees.
- For each tree, get all the paths in the tree and store them. 
- Pick a path from each tree. 
- Swap the paths from the two trees.

Use helper functions to pick the trees, and get the paths. 
"""

import random
from Dataset2.treeInstance_two import grow

MAX_DEPTH = 8

## Determine the paths of the trees (think of them as indices)
def get_tree_paths(tree, current_path = [], paths = None):
    if paths is None: 
        paths = []

    paths.append(current_path)

    if isinstance(tree, tuple):
        operator, left, right = tree
        get_tree_paths(left, current_path + [1], paths)
        get_tree_paths(right, current_path + [2], paths)

    return paths


## Swap the subtrees at the paths from the two trees

# First, retrieve those subtrees at a certain path;
def retrieve_subtree(tree, path):
    node = tree #insert tree into node
    for i in path: #check the directions in the path, when i=1, that's the left node, when i=2, that's the right node.
        node = node[i] #grab the node at position i and re-initialize it to node. So, node now holds a new node(or subtree, or leaf node in some instances)
    return node    #after traversing through that path, return the node at that path.


# Second, then swap the subtrees
def swap_subtrees(tree, path, new_subtree):   #has to return the new tree which has been crossed over
 
    if path == []:
      return new_subtree

    node = tree

    for i in path[:-1]: #traverse the path until we reach the parent of the node we want to replace. 
        node = node[i]  #set the parent node to node. We'll need the parent because in order to change a slot in the tree,
                        #we need to do it through the parent, using its index. (Refer to differences in = with python)

    #Then set the subtree at that spot equal to the new piece: 
    node[path[-1]] = new_subtree   #path[-1] references the last element in the path. so, that's what we swap because it references the node at that path. 
    return tree #editing the node (using the index) also edits the tree 


#Converting a tuple to a list:
def to_list(tree):
    if isinstance(tree, tuple) == False:
        return tree
    #else:
    new_list = []
    for node in tree: 
        new_list.append(to_list(node))
    return new_list



#Converting a list to a tuple: 
def to_tuple(tree):
    if isinstance(tree, list) == False:
        return tree
    #else:
    tree_parts = [] #instead of creating an empty tuple, create an empty list which will keep track
              #of inner tuples (and outer ones as well) and convert them to tuples one by one
              #This is the list-conversion method since we can't append to tuples. 
    for node in tree: 
        tree_parts.append(to_tuple(node))
    return tuple(tree_parts) #convert each list to a tuple. This is reflected in the recursion steps.


#Function to check the depth of a tree --> Helps avoid bloating
def tree_depth(tree, level = 0):
    if isinstance(tree, tuple) == False: #If the tree is leaf, report how far down it is from the root
        return level
    left = tree_depth(tree[1], level + 1)
    right = tree_depth(tree[2], level + 1)
    return max(left, right) #return the level of the deepest leaf 



def crossover(parent1, parent2):

    #First convert parent tuples to lists that are editable: 
    parent1_copy = to_list(parent1)
    parent2_copy = to_list(parent2)

    ## Call paths for parent 1:
    paths_parent1 = get_tree_paths(parent1)
    # Pick a random path to crossover
    path1 = random.choice(paths_parent1)


    ## Call paths for parent 2:
    paths_parent2 = get_tree_paths(parent2)
    # Pick a random path to crossover
    path2 = random.choice(paths_parent2)

    #Find the subtrees at the paths: 
    subtree1 = retrieve_subtree(parent1, path1)
    subtree2 = retrieve_subtree(parent2, path2)

    #call the swap_subtrees function: 
    child1 = swap_subtrees(parent1_copy, path1, subtree2)
    child2 =  swap_subtrees(parent2_copy, path2, subtree1)
    
    child1 = to_tuple(child1)
    child2 = to_tuple(child2)

    #Check if children depths exceed MAXIMUM DEPTH --> To solve the issue of bloating
    if tree_depth(child1) > MAX_DEPTH: #If a child's depth is > max depth, return the parent node instead
        child1 = parent1

    if tree_depth(child2) > MAX_DEPTH:
        child2 = parent2

    return child1, child2



#Mutation function:
def mutate(tree):
    paths = get_tree_paths(tree)                  
    path = random.choice(paths)                
    new_subtree = grow(0, random.randint(0, 2))  
    tree_copy = to_list(tree)  
    mutated_tree = swap_subtrees(tree_copy, path, new_subtree) 
    mutated_tree = to_tuple(mutated_tree)

    #Check mutated tree's depth against the MAX_DEPTH: 
    if tree_depth(mutated_tree) > MAX_DEPTH:
        return tree

    return mutated_tree  #return the mutated tree otherwise

    



#Reproduction function:
def reproduction(tree):
    return tree




"""
#Testing code: 
t = ('+', ('*', 'x', 2), 'y')
for run in range(15):
    print(f"Run {run} | Mutated tree: {mutate(t)}")
print(f"Original tree: {t}")
"""