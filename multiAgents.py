# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # util.raiseNotDefined()
        
        # start the search from the root node, with pacman as the first agent
        return self.minimaxSearch(gameState, 0, 0)[1]

    def minimaxSearch(self, state, depth, agent):
        """
        This function is called whenever a change of turn occurs, i.e. when a ghost or pacman has to make a decision.
        It checks if the conditions to stop the search are met and, if not, calls the appropriate function (maxValue or minValue) to continue.
        """
        
        totalAgents = state.getNumAgents()

        # when every partecipant has moved (the index of the current agent exceeds the total number of agents), restarts from the first one (pacman)
        if agent >= totalAgents:
            agent = 0

        # when the game achieved a terminal state, i.e. the tree has achieved maximum depth or pacman has already won or lost, return the utility 
        if depth == self.depth * totalAgents or state.isWin() or state.isLose():
            return self.evaluationFunction(state), None
        
        if agent == 0:
            # pacman's turn, so we want to maximize the value of the state
            return self.maxValue(state, depth, agent)
        else:
            # ghost's turn, so we want to minimize the value of the state
            return self.minValue(state, depth, agent)
        
    def maxValue(self, state, depth, agent):
        """
        This function is called when Pacman makes a decision: it returns the move that maximizes the cost function value, and the value itself.
        """

        v, move = float("-inf"), None

        # evaluates each possible move's outcome value and chooses the one that maximizes it
        for action in state.getLegalActions(agent):
            v2, a2 = self.minimaxSearch(state.generateSuccessor(agent, action), depth+1, agent+1)

            if v2 > v:
                # if the value of the current state is higher than the previous one, update value and move
                v, move = v2, action
        
        return v, move


    def minValue(self, state, depth, agent):
        """
        This function is called when a ghost makes a decision: it returns the move that minimizes the cost function value, and the value itself.
        """
        
        v, move = float("inf"), None

        # evaluates each possible move's outcome value and chooses the one that minimizes it
        for action in state.getLegalActions(agent):
            v2, a2 = self.minimaxSearch(state.generateSuccessor(agent, action), depth+1, agent+1)

            if v2 < v:
                # if the value of the current state is lower than the previous one, update value and move
                v, move = v2, action
        
        return v, move
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # util.raiseNotDefined()

        # start the search from the root node, with pacman as the first agent and alpha and beta set to negative and positive infinity respectively
        return self.alphabetaSearch(gameState, 0, 0, float("-inf"), float("inf"))[1]

    def alphabetaSearch(self, state, depth, agent, alpha, beta):
        """
        This function is called whenever a change of turn occurs, i.e. when a ghost or pacman has to make a decision.
        It checks if the conditions to stop the search are met and, if not, calls the appropriate function (maxValue or minValue) to continue.
        """

        totalAgents = state.getNumAgents()

        # when every partecipant has moved (the index of the current agent exceeds the total number of agents), restarts from the first one (pacman)
        if agent >= totalAgents:
            agent = 0

       # when the game achieved a terminal state, i.e. the tree has achieved maximum depth or pacman has already won or lost, return the utility 
        if depth == self.depth * totalAgents or state.isWin() or state.isLose():
            return self.evaluationFunction(state), None
        
        if agent == 0:
            # pacman's turn, so we want to maximize the value of the state
            return self.maxValue(state, depth, agent, alpha, beta)
        else:
            # ghost's turn, so we want to minimize the value of the state
            return self.minValue(state, depth, agent, alpha, beta)

    
    def maxValue(self, state, depth, agent, alpha, beta):
        """
        This function is called when Pacman makes a decision: it returns the move that maximizes the cost function value, and the value itself.
        In addition to that, it stops the current search as soon as it obtains a value higher than the min's upper bound.
        It also updates the value of alpha, which represents the max's lower bound.
        """

        v, move = float("-inf"), None
        
        # evaluates each possible move's outcome value and chooses the one that maximizes it
        for action in state.getLegalActions(agent):
            # calls the function recursively for each possible action in order to expand the decision tree
            v2, a2 = self.alphabetaSearch(state.generateSuccessor(agent, action), depth+1, agent+1, alpha, beta)
            
            if v2 > v:
                # if the value of the current state is higher than the previous one, update value, move and alpha
                v, move = v2, action
                alpha = max(alpha, v)

            if v > beta:
                # if the value of the current state is higher than the min's upper bound, return the current value and move
                return v, move
        
        return v, move
    
   
    def minValue(self, state, depth, agent, alpha, beta):
        """
        This function is called when a ghost makes a decision: it returns the move that minimizes the cost function value, and the value itself.
        In addition to that, it stops the current search as soon as it obtains a value lower than the max's upper bound.
        It also updates the value of beta, which represents the min's upper bound.
        """
        
        v, move = float("inf"), None

        # evaluates each possible move's outcome value and chooses the one that minimizes it
        for action in state.getLegalActions(agent):
            # calls the function recursively for each possible action in order to expand the decision tree
            v2, a2 = self.alphabetaSearch(state.generateSuccessor(agent, action), depth+1, agent+1, alpha, beta)
            
            if v2 < v:
                # if the value of the current state is lower than the previous one, update value, move and beta
                v, move = v2, action
                beta = min(beta, v)

            if v < alpha:
                # if the value of the current state is lower than the max's upper bound, return the current value and move
                return v, move
            
        return v, move

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
