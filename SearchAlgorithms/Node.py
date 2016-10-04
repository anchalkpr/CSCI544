class Node:
    
    def __init__(self, nodeLabel):
        self.label = nodeLabel
        self.cost = 0
        self.heuristic = 0
        self.parent = None