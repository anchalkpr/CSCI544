from collections import deque
import heapq
import itertools

def bfs(graph):
    frontier = deque([])
    explored = []
    frontier.append(graph.startNode)
    goalFound = False
    solFound = None
    
    if graph.startNode.label in graph.goalNode:
        goalFound = True
        solFound = graph.startNode
    
    while((len(frontier) > 0) and (goalFound == False)):
        currentNode = frontier.popleft()
        explored.append(currentNode)
        children = graph.adjacency_list[currentNode.label]
        if children:
            for child, cost in children:
                if node_in_frontier(child, frontier) == False and node_in_explored(child, explored) == False:
                    if child.label in graph.goalNode:
                        goalFound = True
                        child.parent = currentNode
                        child.cost = child.parent.cost + 1
                        solFound = child
                        break
                    else:
                        child.parent = currentNode
                        child.cost = child.parent.cost + 1
                        frontier.append(child)
    return solution_path(solFound)
    
def dfs(graph):
    frontier = []
    explored = []
    frontier.append(graph.startNode)
    goalFound = False
    solFound = None
    
    while((len(frontier) > 0) and (goalFound == False)):
        currentNode = frontier.pop()
        if currentNode.label in graph.goalNode:
            goalFound = True
            solFound = currentNode
            break
        explored.append(currentNode)
        children = graph.adjacency_list[currentNode.label]
        children.reverse()
        if children:
            for child, cost in children:
                if node_in_frontier(child, frontier) == False and node_in_explored(child, explored) == False:
                    child.parent = currentNode
                    frontier.append(child)
                    child.cost = child.parent.cost + 1
    return solution_path(solFound)

def ucs(graph):
    counter = itertools.count()
    frontier = [(0, next(counter), graph.startNode)]
    explored = []
    goalFound = False
    solFound = None
    
    while((len(frontier) > 0) and (goalFound == False)):
        cost, count, currentNode = heapq.heappop(frontier)
        if currentNode.label in graph.goalNode:
            goalFound = True
            solFound = currentNode
            break
        explored.append(currentNode)
        children = graph.adjacency_list[currentNode.label]
        if children:
            for child, pathcost in children:
                if node_in_frontier_ucs(child, frontier) == False and node_in_explored(child, explored) == False:
                    child.parent = currentNode
                    child.cost = child.parent.cost + pathcost
                    heapq.heappush(frontier, (child.cost, next(counter), child))
                elif node_in_frontier_ucs(child, frontier):
                    frontier_index = get_ucs_frontier_node_index(child, frontier)
                    previous_child_cost = frontier[frontier_index][0]
                    new_child_cost = currentNode.cost + pathcost
                    if new_child_cost < previous_child_cost:
                        child.parent = currentNode
                        child.cost = new_child_cost
                        frontier[frontier_index] = (new_child_cost, next(counter), child)
                        heapq.heapify(frontier)
                elif node_in_explored(child, explored):
                    explored_index = get_explored_node_index(child, explored)
                    previous_child_cost = child.cost
                    new_child_cost = currentNode.cost + pathcost
                    if new_child_cost < previous_child_cost:
                        del explored[explored_index]
                        child.parent = currentNode
                        child.cost = new_child_cost
                        heapq.heappush(frontier, (child.cost, next(counter), child))
    return solution_path(solFound)

def astar(graph):
    counter = itertools.count()
    frontier = [(0, next(counter), graph.startNode)]
    explored = []
    goalFound = False
    solFound = None
    
    while((len(frontier) > 0) and (goalFound == False)):
        cost, count, currentNode = heapq.heappop(frontier)
        if currentNode.label in graph.goalNode:
            goalFound = True
            solFound = currentNode
            break
        explored.append(currentNode)
        children = graph.adjacency_list[currentNode.label]
        if children:
            for child, pathcost in children:
                if node_in_frontier_ucs(child, frontier) == False and node_in_explored(child, explored) == False:
                    child.parent = currentNode
                    child.cost = child.parent.cost + pathcost
                    heapq.heappush(frontier, (child.cost + child.heuristic, next(counter), child))
                elif node_in_frontier_ucs(child, frontier):
                    frontier_index = get_ucs_frontier_node_index(child, frontier)
                    previous_child_cost = child.cost
                    new_child_cost = currentNode.cost + pathcost
                    if new_child_cost < previous_child_cost:
                        child.parent = currentNode
                        child.cost = new_child_cost
                        frontier[frontier_index] = (new_child_cost + child.heuristic, next(counter), child)
                        heapq.heapify(frontier)
                elif node_in_explored(child, explored):
                    explored_index = get_explored_node_index(child, explored)
                    previous_child_cost = child.cost
                    new_child_cost = currentNode.cost + pathcost
                    if new_child_cost < previous_child_cost:
                        del explored[explored_index]
                        child.parent = currentNode
                        child.cost = new_child_cost
                        heapq.heappush(frontier, (new_child_cost + child.heuristic, next(counter), child))
    return solution_path(solFound)

def get_ucs_frontier_node_index(child, frontier):
    for cost, count, node in frontier:
        if node.label == child.label:
            return frontier.index((cost, count, node))
        
def get_explored_node_index(child, explored):
    for node in explored:
        if node.label == child.label:
            return explored.index(node)   
                
def node_in_frontier(child, frontier):
    if child in frontier:
        return True
    else:
        return False

def node_in_frontier_ucs(child, frontier):
    found = False
    for cost, count, node in frontier:
        if node.label == child.label:
            found = True
    return found

def node_in_explored(child, explored):
    if child in explored:
        return True
    else:
        return False

def solution_path(node):
    sol = []
    while node:
        sol_str = "%s %s" %(node.label, node.cost)
        sol.append(sol_str)
        node = node.parent
    sol.reverse()
    return sol