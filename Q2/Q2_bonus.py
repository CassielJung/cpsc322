from sys import maxsize as MAXINT

# Name:         calcPathCost
# Purpose:      Calculate cost of the given path
# Parameter:    path - string representing path to calculate cost
# Return:       cost of the path
def calcPathCost(path:str):
    edges = {
        'SA':3, 'SB':9, 'SC':4, 'AC':2, 'BC':13,
        'CD':5, 'CE':4, 'CF':8, 'DF':5, 'EF':7,
        'FG':8, 'FH':7, 'FZ':18, 'GZ':9, 'HZ':6
    }

    pathCost = 0
    for i in range(len(path)-1):
        subPath = path[i]+path[i+1]
        pathCost += edges[subPath]

    return pathCost

# Name:         getHeuristic
# Purpose:      Get heuristic value of the given node
# Parameter:    node - character representing a node
# Return:       heuristic values
def getHeuristic(node:str):
    heuristics = {
        'S': 24, 'A': 21, 'B': 19, 'C': 19, 'D': 9, 'E': 11,
        'F': 12, 'G': 4, 'H': 6, 'Z': 0
    }
    return heuristics.get(node)

# Name:         calcFVal
# Purpose:      Calculate f(p) value [f(p) = cost(p)+h(p)]
# Parameter:    path - path to calculate f(path) value
# Return:       f(p) value
def calcFVal(path:str):
    return calcPathCost(path)+getHeuristic(path[-1])

# Name:         Frontier
# Purpose:      Wrapper class to represent frontier
class Frontier:
    def __init__(self, algorithm:str, bound:int=-1):        # Initialize bound to -1 since it won't be used other than IDS
        self.algorithm = algorithm
        self.frontier = []
        self.bound = bound

    # Name:         isEmpty
    # Purpose:      Check if frontier is empty
    # Parameter:    None
    # Return:       True if frontier is empty False otherwise
    def isEmpty(self):
        return False if self.frontier else True

    # Name:         push
    # Purpose:      push given path
    # Parameter:    path - string to represent path
    # Return:       None
    def push(self, path):
        cost = 0                                            # Initialize cost value for not-informed algorithms
        if self.algorithm == 'IDS':                         # Check bound when IDS
            if len(path) > self.bound+1:                    # if current path length > bound, do not add to frontier
                return
        elif self.algorithm == 'LCFS':
            cost = calcPathCost(path)
        elif self.algorithm == 'BestFS':
            cost = getHeuristic(path[-1])
        elif self.algorithm == 'A*':
            cost = calcFVal(path)

        self.frontier.append((path, cost))           

        if self.algorithm in ('LCFS', 'BestFS', 'A*'):      # sort if priority queue
            self.frontier = sorted(self.frontier, key=lambda tup: tup[1])

    # Name:         pop
    # Purpose:      Pop appropriate element from the frontier
    # Parameter:    None
    # Return:       pop-ed path from the frontier or None
    def pop(self):
        if not self.isEmpty():
            if self.algorithm in ('DFS', 'IDS', 'B&B'):     # stack
                return self.frontier.pop()[0]
            else:                                           # queue / priority queue
                return self.frontier.pop(0)[0]
        else:
            print("Frontier was empty")
            return None

# Name:         getAdjacent
# Purpose:      Get adjacent nodes of the given node
# Parameter:    graph - dict representing graph
#               node - string to represent node
# Return:       adjacent nodes
def getAdjacent(graph:dict, node:str):
    adjacents = graph.get(node)
    nodes = [tup[0] for tup in adjacents]
    return nodes

# Name:         search
# Purpose:      search for a path from start to goal
# Parameter:    graph - dict representing graph
#               frontier - Frontier class representing frontier of the search algorithm
#               start/goal - start and goal node to find the path for
# Return:       
def search(graph: dict, frontier: Frontier, start:str, goal:str):
    frontier.push(start)

    while not frontier.isEmpty():
        currPath = frontier.pop()
        currNode = currPath[-1]
        print("Expand Node:", currNode)

        if currNode == goal:
            return currPath
        else:
            for item in getAdjacent(graph, currNode):
                newPath = currPath + item[0]
                frontier.push(newPath)
    
    return None

# Name:         IDS
# Purpose:      run IDS algorithm on given graph
# Parameter:    graph - dict representing graph
#               start/goal - start and goal node
# Return:       path found
def IDS(graph: dict, start:str, goal:str):
    path = None

    bound = 0
    while not path:
        bound += 1
        frontier = Frontier('IDS', bound)
        path = search(graph, frontier, start, goal)

    return path

# Name:         bAndB
# Purpose:      run B&B algorithm on given graph
# Parameter:    graph - dict representing graph
#               start/goal - start and goal node
# Return:       solution path found
def BandB(graph: dict, start:str, goal:str):
    frontier = Frontier("B&B")
    frontier.push(start)
    upperBound = MAXINT
    bestPath = ""

    while not frontier.isEmpty():
        currPath = frontier.pop()

        if calcFVal(currPath) >= upperBound:
            pass
        else:
            currNode = currPath[-1]
            print("Expand Node:", currNode)

            if currNode == goal:
                bestPath = currPath
                upperBound = calcPathCost(currPath)
            else:
                for item in getAdjacent(graph, currNode):
                    newPath = currPath + item[0]
                    frontier.push(newPath)

    return bestPath

if __name__ == "__main__":
    Graph = {
            'S': ['A','B','C'],
            'A': ['C'],
            'B': ['C'],
            'C': ['D','E','F'],
            'D': ['F'],
            'E': ['F'],
            'F': ['G','H','Z'],
            'G': ['Z'],
            'H': ['Z'],
        }
    start = 'S'
    goal = 'Z'

    frontierList = [Frontier('DFS'), Frontier('BFS'), Frontier('LCFS'), Frontier('BestFS'), Frontier('A*')]

    for frontier in frontierList:
        print(f"Run {frontier.algorithm}")
        searchResult = search(Graph, frontier, start, goal)
        if searchResult:
            print(searchResult,"\n")

    print("Run IDS")
    idsResult = IDS(Graph, start, goal)
    if idsResult:
        print(idsResult, "\n")

    print("Run B&B")
    bAndBResult = BandB(Graph, start, goal)
    if bAndBResult:
        print(bAndBResult)