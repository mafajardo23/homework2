import random 

## Set up the building blocks
OPERATORS = ['+', '-' , '*', '/'] #non-terminal
VARIABLES = ['x'] #terminal --> No chid nodes. 
CONSTANTS = range(-4,4) #terminal

## Set up a function that picks a random terminal (constant or variable)
def pick_random_terminal():
    ## Essentially, flip a coin to see which set of terminals to pick from
    ## That is, if heads, then choose a random from variables, otherwise, pick from constants
    ## Let's start with a fair coin; we can change this if we find that there are more x's than values
    if random.random() < 0.5: ##the first half (heads)
        return random.choice(VARIABLES) #pick a variable
    return random.choice(CONSTANTS) #else, pick a constant

## Assemble the tree using operators and terminals
## MAX_DEPTH = 2
def grow(level, max_depth): #start from a certain depth level e.g. where depth = 0
    if level == max_depth: ## If we're at the last node depth, pick a terminal
        node = pick_random_terminal()
    else: 
        operator = random.choice(OPERATORS) #else, pick an operator
        left_node = grow(level+1, max_depth)
        right_node = grow(level+1, max_depth)
        node = (operator, left_node, right_node)
    return node


##tree = grow(0, 2)
tree = grow(0,3)
print(tree)

