"""
Crossover logic:
- Pick two trees.
- For each tree, get all the paths in the tree and store them. 
- Pick a path from each tree. 
- Swap the paths from the two trees.

Use helper functions to pick the trees, and get the paths. 

NB: Remember to store the new functions tht 
"""

import random


## Step 2: Determine the paths of the trees (think of them as indices)
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

#subtree1 = retrieve_subtree(parent1, path1)
#subtree2 = retrieve_subtree(parent2, path2)


# Second, then swap the subtrees
def swap_subtrees(tree, path, new_subtree):   #has to return the new tree which has been crossed over
 
    #we want to edit the tree but its a tuple, so change it to a list
    #node = to_list(tree)
    if path == []:
      return new_subtree

    node = tree

    ##DOUBLE CHECK TRAVERSING THROUGH THE TREE ITSELF.

    for i in path[:-1]: #traverse the path until we reach the parent of the node we want to replace. 
        node = node[i]  #set the parent node to node. We'll need the parent because in order to change a slot in the tree,
                        #we need to do it through the parent, using its index. (Refer to differences in = with python)

    #Then set the subtree at that spot equal to the new piece: 
    node[path[-1]] = new_subtree   #path[-1] references the last element in the path. so, that's what we swap because it references the node at that path. 
    return tree #editing the node (using the index) also edits the tree 




def crossover(parent1, parent2):
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


    #Make copies of the parent trees to turn them into lists that are editable
    parent1_copy = list(parent1)
    parent2_copy = list(parent2)

    #call the swap_subtrees function: 
    child1 = swap_subtrees(parent1_copy, path1, subtree2)
    child2 =  swap_subtrees(parent2_copy, path2, subtree1)

    return tuple(child1), tuple(child2)

