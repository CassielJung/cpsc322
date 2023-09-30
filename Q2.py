# Graph class to represent graph at Assignment2, Question2
class Graph:
    def __init__(self):
        # key - node, value - adjacent node
        self.graph = {
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

    def getAdjacent(self, node:str):
        return self.graph.get(node)
    
class Frontier:
    def __init__(self, algorithm:str):        # Initialize bound to -1 since it won't be used other than IDS
        self.algorithm = algorithm
        self.frontier = []

    def isEmpty(self):
        return False if self.frontier else True

    def push(self, item:str):
        self.frontier.append(item)

    def pop(self):
        if not self.isEmpty():
            if self.algorithm in ('DFS'):       # stack
                return self.frontier.pop()
            elif self.algorithm in ('BFS'):     # queue
                return self.frontier.pop(0)
        else:
            print("Frontier was empty")

    def getFrontier(self):
        return self.frontier

def search(graph: Graph, frontier: Frontier, start:str, goal:str):
    frontier.push(start)

    while not frontier.isEmpty():
        currPath = frontier.pop()
        currNode = currPath[-1]
        print("Expand Node:", currNode)

        if currNode == goal:
            return currPath
        else:
            for item in graph.getAdjacent(currNode):
                newPath = currPath + item[0]
                frontier.push(newPath)
    
    return None

if __name__ == "__main__":
    graph = Graph()

    print("Run DFS")
    dfsFrontier = Frontier('DFS')
    dfsResult = search(graph, dfsFrontier, 'S', 'Z')
    if dfsResult:
        print(dfsResult)

    print("\nRun BFS")
    bfsFrontier = Frontier('BFS')
    bfsResult = search(graph, bfsFrontier, 'S', 'Z')
    if bfsResult:
        print(bfsResult)