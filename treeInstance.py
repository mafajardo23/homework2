import random 

## Set up the building blocks
OPERATORS = ['+', '-' , '*', '/'] #non-terminal
VARIABLES = ['x'] #terminal --> No chid nodes. 
CONSTANTS = range(-1,1) #terminal

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
#tree = grow(0,3)
#print(tree)

def traversal(node, x):
    #We can't the final step without knowing thats in the left tree and whats on the right tree. Recursively
    # base case 1: the variable
    if node == 'x':
        return x

    # base case 2: a constant
    if type(node) == int or type(node) == float:
        return node

    # recursive case: unpack the operator tuple
    operator = node[0]
    left = node[1]
    right = node[2]


    # get the left answer and the right answer (recursion!)
    left_result = traversal(left, x)
    right_result = traversal(right, x)

    # check which operator it is, do that math, return it
    if operator == '+':
        return left_result + right_result
    elif operator == '-':
        return left_result - right_result
    elif operator == '*':
        return left_result * right_result
    elif operator == '/':
        if right_result == 0:
            return 1 #return 1 if the denominator is 0
        else:
            return left_result / right_result

def reproduction(tree):
    return tree

        
if __name__ == "__main__":
    test = ('-', ('*', 'x', 2), ('/', 'x', 'x'))
    print(traversal(test, 3))       # should print 5

    test2 = ('+', ('*', 'x', 'x'), 3)
    print(traversal(test2, 2))      # should print 7

    div_zero = ('/', 'x', ('-', 'x', 'x'))
    print(traversal(div_zero, 4))   # should print 1