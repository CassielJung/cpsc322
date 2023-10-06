DEBUG = False

if DEBUG:
    VARIABLE_LIST = ['X', 'Y', 'Z']
    DOMAIN = ('t', 'f')
else:
    VARIABLE_LIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']                # Variable ordering without heuristics
    # VARIABLE_LIST = ['F', 'H', 'C', 'D', 'G', 'E', 'A', 'B']              # Variable ordering with heuristics
    DOMAIN = (1, 2, 3, 4)

def search():
    # Initialize variables
    frontier = list()
    searchTree = list()
    solutions = list()
    numFailedBranch: int = 0

    # Append first nodes to frontier
    for elem in DOMAIN:
        frontier.append([elem])

    while len(frontier) != 0:
        # Get a model from frontier
        currModel = frontier.pop()

        # Check if current model meet constraints
        if checkConstraints(currModel):
            # if all variables are not assigned yet
            if len(currModel) != len(VARIABLE_LIST):
                # assign value to one more variable
                for elem in DOMAIN:
                    frontier.append(currModel+[elem])
            else:
                # current model is the solution append it to both search tree and solution
                searchTree.append(currModel+['solution'])
                solutions.append(dict(zip(VARIABLE_LIST, currModel)))
        else:
            searchTree.append(currModel+['failure'])
            numFailedBranch += 1
    
    # Generate search tree
    print('Search Tree:')
    printSearchTree(searchTree)

    # Print solutions found
    print('\nSolutions:')
    for sol in solutions:
        print(sol)

    # Print the number of failed branch
    print('\nNum Failed Branch:', numFailedBranch)

def checkConstraints(model: list):
    # Hardcode contraints
    constraints: dict = {
        ('A', 'G'): (lambda a, g: a > g),
        ('A', 'H'): (lambda a, h: a <= h),
        ('B', 'F'): (lambda b, f: abs(f-b)==1),
        ('G', 'H'): (lambda g, h: g < h),
        ('C', 'G'): (lambda c, g: abs(g-c)==1),
        ('C', 'H'): (lambda c, h: abs(h-c)%2==0),
        ('D', 'H'): (lambda d, h: h != d),
        ('D', 'G'): (lambda d, g: d >= g),
        ('C', 'D'): (lambda c, d: d != c),
        ('C', 'E'): (lambda c, e: e != c),
        ('D', 'E'): (lambda d, e: e < (d-1)),
        ('E', 'H'): (lambda e, h: e != (h-2)),
        ('F', 'G'): (lambda f, g: g != f),
        ('F', 'H'): (lambda f, h: h != f),
        ('C', 'F'): (lambda c, f: c != f),
        ('D', 'F'): (lambda d, f: d != (f-1)),
        ('E', 'F'): (lambda e, f: abs(e-f)%2==1),

        ('X', 'Y'): (lambda x, y: x != y),              # Constraints for debugging
        ('Y', 'Z'): (lambda y, z: y != z)
    }

    # Initialize constraint status
    meetConstraints: bool = True

    # Loop through current model to check constraints
    for idx1 in range(len(model)-1):
        var1 = VARIABLE_LIST[idx1]
        elem1 = model[idx1]
        for idx2 in range(idx1+1, len(model)):
            var2 = VARIABLE_LIST[idx2]
            elem2 = model[idx2]

            # Sort variable in the alphabetical order to search constraint
            pair = sorted([(var1, elem1), (var2, elem2)])
            key = (pair[0][0], pair[1][0])
            values = (pair[0][1], pair[1][1])

            # If key exist in the constraints dict
            if constraints.get(key):
                # Check constraints
                meetConstraints = constraints[key](values[0], values[1])

                # If failed to meet constraints, return False
                if not meetConstraints:
                    return meetConstraints
                
    return meetConstraints

def printSearchTree(searchTree: list):
    # print first branch to intialize prevBranch
    prevBranch = searchTree[0]
    for i, elem in enumerate(prevBranch):
        if i != len(prevBranch)-1:
            print(f"{VARIABLE_LIST[i]}={elem}", end=' ')
        else:
            print(elem)

    # print rest of the branches
    for branch in searchTree[1:]:
        # loop through varaible assigned through branch
        for i, elem in enumerate(branch):
            # if element is not a status code (failure or solution)
            if i != len(branch)-1:
                try:
                    if elem != prevBranch[i]:
                        print(f"{VARIABLE_LIST[i]}={elem}", end=' ')
                    else:
                        print("   ", end=' ')
                except:
                    print(f"{VARIABLE_LIST[i]}={elem}", end=' ')
            else:
                print(elem)
        prevBranch = branch

if __name__ == "__main__":
    search()