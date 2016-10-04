from GraphAdjacencyList import GraphAdjacencyList
from Node import Node
from SearchAlgos import bfs, dfs, ucs, astar

def solve_problem():
    inputFile = open("input.txt", 'r')
    lines = inputFile.readlines()
    inputFile.close()
    algorithm = lines[0].strip()
    startState = lines[1].strip()
    goalState = lines[2].strip().split()
    edgeCount = int(lines[3].strip())
    edgeStartIndex = 4
    edgeEndIndex = edgeStartIndex + edgeCount - 1
    heuristicListCount = int(lines[edgeEndIndex + 1].strip())
    heuristicStartIndex = edgeEndIndex + 2
    heuristicEndIndex = heuristicStartIndex + heuristicListCount - 1
    nodeList = {}
    for line in lines[edgeStartIndex: edgeEndIndex + 1]:
        index = lines.index(line)
        line = line.strip().split(" ")
        lines[index] = line
        if line[0] not in nodeList.keys():
            nodeList[line[0]] = Node(line[0])
        if line[1] not in nodeList.keys():
            nodeList[line[1]] = Node(line[1])
            
    for line in lines[heuristicStartIndex: heuristicEndIndex + 1]:
        line = line.strip().split(" ")
        nodeList[line[0]].heuristic = int(line[1])
        
    startNode = nodeList[startState]
    graph = GraphAdjacencyList(startNode, goalState, nodeList)
        
    for line in lines[edgeStartIndex: edgeEndIndex + 1]:
        graph.addEdge(line[0], line[1], int(line[2]))
    
    output = []
    
    if algorithm == "BFS":
        output = bfs(graph)
    elif algorithm == "DFS":
        output = dfs(graph)
    elif algorithm == "UCS":
        output = ucs(graph)
    elif algorithm == "A*":
        output = astar(graph)
    print output
    printoutput(output)

def printoutput(output):
    outputFile = open("output.txt", 'w')
    outputFile.write("\n".join(output))
    outputFile.close()
    
solve_problem()     
    