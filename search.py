# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from cmath import inf
from itertools import accumulate
from queue import PriorityQueue
import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# Please DO NOT change the following code, we will use it later
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    myPQ = util.PriorityQueue()
    startState = problem.getStartState()
    startNode = (startState, '',0, [])
    myPQ.push(startNode,heuristic(startState,problem))
    visited = set()
    best_g = dict()
    while not myPQ.isEmpty():
        node = myPQ.pop()
        state, action, cost, path = node
        if (not state in visited) or cost < best_g.get(state):
            visited.add(state)
            best_g[state]=cost
            if problem.isGoalState(state):
                path = path + [(state, action)]
                actions = [action[1] for action in path]
                del actions[0]
                return actions
            for succ in problem.getSuccessors(state):
                succState, succAction, succCost = succ
                newNode = (succState, succAction, cost + succCost, path + [(state, action)])
                myPQ.push(newNode,heuristic(succState,problem)+cost+succCost)
    util.raiseNotDefined()




def improve(improveNode, problem, heuristic=nullHeuristic):
    Q = util.Queue()
    Q.push(improveNode)
    closed = set()
    while not Q.isEmpty():
        tempNode = Q.pop()
        state, action, cost, path = tempNode
        if not state in closed:
            closed.add(tempNode[0])
            if heuristic(tempNode[0], problem) < heuristic(improveNode[0], problem):
                return tempNode
            for succ in problem.getSuccessors(tempNode[0]):
                succState, succAction, succCost = succ
                newNode = (succState, succAction, cost + succCost, path + [action])
                Q.push(newNode)


def enforcedHillClimbing(problem, heuristic=nullHeuristic):
    """
    Local search with heuristic function.
    You DO NOT need to implement any heuristic, but you DO have to call it.
    The heuristic function is "manhattanHeuristic" from searchAgent.py.
    It will be pass to this function as second argument (heuristic).
    """

    
    # The improve function for supporting enforced Hill Climbling

    initialState = problem.getStartState()
    startNode = (initialState, '', 0, [])
    iterNode = startNode
    
    while not problem.isGoalState(iterNode[0]):
        iterNode = improve(iterNode, problem, heuristic)

    # find the goal state and break, so now the iterNode is the goal state    
    state, action, cost, path = iterNode
    # the last action haven't been added to the path, since already breaks the while loop
    iterNode[3].append(action)
    del iterNode[3][0]
    return iterNode[3]
        
    
    
    # put the below line at the end of your code or remove it
    util.raiseNotDefined()
        



from math import inf as INF   
def bidirectionalAStarEnhanced(problem, heuristic=nullHeuristic, backwardsHeuristic=nullHeuristic):
    
    """
    Bidirectional global search with heuristic function.
    You DO NOT need to implement any heuristic, but you DO have to call them.
    The heuristic functions are "manhattanHeuristic" and "backwardsManhattanHeuristic" from searchAgent.py.
    It will be pass to this function as second and third arguments.
    You can call it by using: heuristic(state,problem) or backwardsHeuristic(state,problem)
    """
    

    # since it may reopen under some condition, so we need to create set to store states and priority queue to store nodes

    # Open and closed list of forward and backaward
    
    # Priority Queue of forwards and backward
    openPQ_f = util.PriorityQueue()
    openPQ_b = util.PriorityQueue()

    # closed list : the states that have been visited = visited set in A* example
    closed_f = set()
    closed_b = set()

    # lower bound and upper bound
    Low = 0
    Up = INF

    # the final solution of path
    solution = []
    
    # direction to search
    x = "forward"

    # intial state
    initialState = problem.getStartState()
    # initial node - state, action, cost
    startNode = (initialState, [], 0)
    
    # goal state
    goalState = problem.getGoalStates()
    
    # need dictionary to store value for g(n) and path for achieving it,
    # in order to check whether soem better g(n) appears
    fgn = dict()
    bgn = dict()

    # add intial state to g(n) dictionary
    fgn[str(initialState)] = (0, [])


    # Since there maybe not only one goal state, so we need to add them all
    for goal in goalState:
        bgn[str(goal)] = (0, [])


    # add initial and final nodes into the priority queue
    openPQ_f.push(startNode, heuristic(initialState, problem))
    for goal in goalState:
        # goal node - state, action, cost
        goalNode = (goal, [], 0)
        openPQ_b.push(goalNode, backwardsHeuristic(goal, problem))
        

    # implement the algorithm
    while not openPQ_f.isEmpty() and not openPQ_b.isEmpty():
        bminf = openPQ_f.getMinimumPriority()
        bminb = openPQ_b.getMinimumPriority()
        # update Lower bound
        Low = (bminf + bminb)/2
        
        # depends on differnt condtion, the node will pop out from different priority queue
        if(x == "forward"):
            tempNode = openPQ_f.pop()
            state, actions, cost = tempNode

            # if the g(n) dictionary of forward direction has already contains the state and the g(n) value is larger than current Value
            # or the g(n) dictionary actually doesn't contain this state (which means this state hasn't been visited)

            # then add it (or update it) in g(n) of forward direction
            if (str(state) not in closed_f) or (cost < fgn[str(state)][0]):
                closed_f.add(str(state))
                fgn[str(state)] = (cost, actions)

            # if current traverse go into the state that the opposite direction has visited
            if (str(state) in closed_b) and fgn[str(state)][0] + bgn[str(state)][0]  < Up:
                Up = fgn[str(state)][0] + bgn[str(state)][0]
                backward_path = list(reversed(bgn[str(state)][1]))
                solution = fgn[str(state)][1] + backward_path

            if Low >= Up:
                return solution
            
            # calculate the df(n)
            dforward = fgn[str(state)][0] - backwardsHeuristic(state, problem)

            for succ in problem.getSuccessors(state):
                sState, sAction, sCost = succ
                if str(sState) not in closed_f:
                    # f(n') = the h-value of current state + cost of current state + cost of successor state
                    bfn = heuristic(sState, problem) + sCost + cost + dforward
                    inNode = (sState, actions+[sAction], cost+sCost)
                    openPQ_f.push(inNode, bfn)


        elif(x=="backward"):
            tempNode = openPQ_b.pop()
            state, actions, cost = tempNode

            # if the g(n) dictionary of backward direction has already contains the state and the g(n) value is larger than current Value
            # or the g(n) dictionary actually doesn't contain this state (which means this state hasn't been visited)

            # then add it (or update it) in g(n) of backward direction
            if str(state) not in closed_b or cost < bgn[str(state)][0]:
                closed_b.add(str(state))
                bgn[str(state)] = (cost, actions)

            # if current traverse go into the state that the opposite direction has visited
            if (str(state) in closed_f) and fgn[str(state)][0] + bgn[str(state)][0]  < Up:
                Up = fgn[str(state)][0] + bgn[str(state)][0]
                backward_path = list(reversed(bgn[str(state)][1]))
                solution = fgn[str(state)][1] + backward_path

            if Low >= Up:
                return solution

            # calculate the db(n)
            dbackward = bgn[str(state)][0] - heuristic(state, problem)
        
            for succ in problem.getBackwardsSuccessors(state):
                sState, sAction, sCost = succ
                if str(sState) not in closed_b:
                    # f(n') = the h-value of current state + cost of current state + cost of successor state
                    bbn = backwardsHeuristic(sState,problem) + sCost + cost + dbackward
                    inNode = (sState, actions+[sAction], cost+sCost)
                    openPQ_b.push(inNode, bbn)

        if(bminf < bminb):
            x = "forward"
        else:
            x = "backward"

    # put the below line at the end of your code or remove it
    util.raiseNotDefined()









# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


ehc = enforcedHillClimbing
bae = bidirectionalAStarEnhanced


