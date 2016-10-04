class GraphAdjacencyList:
    
    def __init__(self, startNode, goalNode, nodeList):
        self.adjacency_list = {}
        self.startNode = startNode
        self.goalNode = goalNode
        self.nodeList = nodeList
        for state in nodeList:
            self.adjacency_list.update({state : []})
        
    def addEdge(self, source, dest, cost):
        self.adjacency_list[source].append((self.nodeList[dest], cost))
        