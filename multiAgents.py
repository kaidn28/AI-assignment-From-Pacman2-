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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        score=successorGameState.getScore()
        foodArray=newFood.asList()
        alpha = 1.5
        for i in foodArray:
          foodDist = util.manhattanDistance(i,newPos)
          if (foodDist)!=0:
            score += alpha/foodDist

        for ghost in newGhostStates:
          ghostpos=ghost.getPosition()
          ghostDist = util.manhattanDistance(ghostpos,newPos)
          if ghostDist > 0:
            score -= 1.0/ghostDist
        return score

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
        """
        "*** YOUR CODE HERE ***"

        result = self.get_value(gameState, 0, 0) #score + action

        return result[1]

    def get_value(self, gameState, index, depth):
      
      # terminal state:
      if len(gameState.getLegalActions(index)) == 0 or depth == self.depth:
        return gameState.getScore(), ""

      if index == 0:
        return self.max_value(gameState, index, depth)

      else:
        return self.min_value(gameState, index, depth)

    def max_value(self, gameState, index, depth):
        
      legalMoves = gameState.getLegalActions(index)
      max_value = float("-inf")
      max_action = ""

      for action in legalMoves:
        successor = gameState.generateSuccessor(index, action)
        successor_index = index + 1
        successor_depth = depth

        if successor_index == gameState.getNumAgents():
          successor_index = 0
          successor_depth += 1

        current_value = self.get_value(successor, successor_index, successor_depth)[0]

        if current_value > max_value:
          max_value = current_value
          max_action = action

      return max_value, max_action

    def min_value(self, gameState, index, depth):
      legalMoves = gameState.getLegalActions(index)
      min_value = float("inf")
      min_action = ""

      for action in legalMoves:
        successor = gameState.generateSuccessor(index, action)
        successor_index = index + 1
        successor_depth = depth

        # Update the successor agent's index and depth if it's pacman
        if successor_index == gameState.getNumAgents():
          successor_index = 0
          successor_depth += 1

        current_value = self.get_value(successor, successor_index, successor_depth)[0]

        if current_value < min_value:
          min_value = current_value
          min_action = action

      return min_value, min_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, game_state):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # Format of result = [action, score]
        # Initial state: index = 0, depth = 0, alpha = -infinity, beta = +infinity
        result = self.getBestActionAndScore(game_state, 0, 0, float("-inf"), float("inf"))

        # Return the action from result
        return result[0]

    def getBestActionAndScore(self, game_state, index, depth, alpha, beta):
        # Terminal states:
      if len(game_state.getLegalActions(index)) == 0 or depth == self.depth:
        return "", game_state.getScore()

        
      if index == 0:
        return self.max_value(game_state, index, depth, alpha, beta)

      else:
        return self.min_value(game_state, index, depth, alpha, beta)

    def max_value(self, game_state, index, depth, alpha, beta):
        
      legalMoves = game_state.getLegalActions(index)
      max_value = float("-inf")
      max_action = ""

      for action in legalMoves:
        successor = game_state.generateSuccessor(index, action)
        successor_index = index + 1
        successor_depth = depth

        # Update the successor agent's index and depth if it's pacman
        if successor_index == game_state.getNumAgents():
          successor_index = 0
          successor_depth += 1

        # action + score for the current successor
        current_action, current_value \
          = self.getBestActionAndScore(successor, successor_index, successor_depth, alpha, beta)

        # Update max_value and max_action for maximizer agent
        if current_value > max_value:
          max_value = current_value
          max_action = action

        alpha = max(alpha, max_value)

        if max_value > beta:
          return max_action, max_value

      return max_action, max_value

    def min_value(self, game_state, index, depth, alpha, beta):
        
      legalMoves = game_state.getLegalActions(index)
      min_value = float("inf")
      min_action = ""

      for action in legalMoves:
        successor = game_state.generateSuccessor(index, action)
        successor_index = index + 1
        successor_depth = depth

         
        if successor_index == game_state.getNumAgents():
          successor_index = 0
          successor_depth += 1

          #action+score of current successor
        current_action, current_value \
          = self.getBestActionAndScore(successor, successor_index, successor_depth, alpha, beta)

          # Update min_value and min_action
        if current_value < min_value:
          min_value = current_value
          min_action = action

        beta = min(beta, min_value)

        if min_value < alpha:
          return min_action, min_value

      return min_action, min_value

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

