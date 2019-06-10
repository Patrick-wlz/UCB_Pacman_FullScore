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
        
        from math import sqrt
        sum_ = 0
        newFood = newFood.asList()
        currFood = currentGameState.getFood().asList()

        ghost_distances = []
        if successorGameState.isLose():
            return -9999999

        for ghost_position in successorGameState.getGhostPositions():
            ghost_distances.append(manhattanDistance(newPos, ghost_position))
        min_ghost_distance = min(ghost_distances)

        danger = 0
        if min_ghost_distance < 2:
            danger -= 999999
        elif action == 'Stop':
            return -999999

        total_food_distance = 0
        average_food_distance = 0
        food_distances = []
        if newFood:
            for food in newFood:
                total_food_distance += sqrt(float(manhattanDistance(newPos, food) + 1.0))
                food_distances.append(sqrt(float(manhattanDistance(newPos, food) + 1.0)))
            average_food_distance = total_food_distance/len(newFood)

        min_food_distance = 0
        if food_distances:
            min_food_distance += min(food_distances)

        score_change = successorGameState.getScore() - currentGameState.getScore()

        strong_time = 0
        for time_ in newScaredTimes:
            strong_time += time_

        eat = 0
        if newPos in currFood:
            eat += 100000
        sum_ = eat + danger + strong_time - 0.9*min_food_distance - 0.2*average_food_distance + 0.3*sqrt(min_ghost_distance) + score_change
        return sum_
        #return successorGameState.getScore()

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
        n = gameState.getNumAgents()
        depth_ = self.depth

        def minimax(state, depth, currdep=-1, number=n):
            currdep += 1
            if depth*n == currdep or state.isLose() or state.isWin():
                return self.evaluationFunction(state), "Stop"
            if currdep % n == 0:
                max_value = -999999
                move_ = ""
                for action in state.getLegalActions(0):
                    value_ = minimax(state.generateSuccessor(0, action), depth, currdep, number)[0]
                    if value_ > max_value:
                        max_value = value_
                        move_ = action
                return max_value, move_

            else:
                index = currdep % n
                min_value = 999999

                for action in state.getLegalActions(index):
                    value_ = minimax(state.generateSuccessor(index, action), depth, currdep, number)[0]
                    if value_ < min_value:
                        min_value = value_

                return min_value, " "

        result = minimax(gameState, depth_, -1, n)[1]
        return result
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numb = gameState.getNumAgents()
        dep = self.depth

        def alpha_beta(state, depth, alpha, beta, index, n=numb, depth_=dep):
            if depth == depth_ or state.isWin() or state.isLose():
                return self.evaluationFunction(state), " "

            if index == 0:
                max_value = -999999.0
                move_ = " "
                for action in state.getLegalActions(0):
                    value = alpha_beta(state.generateSuccessor(0, action), depth, alpha, beta, (index + 1) % n)[0]
                    if value > max_value:
                        max_value = value
                        move_ = action
                        if max_value > beta:
                            return max_value, move_
                        if alpha < max_value:
                            alpha = max_value
                return max_value, move_

            else:
                min_value = 99999999
                if index == n - 1:
                    depth += 1
                for action in state.getLegalActions(index):
                    value = alpha_beta(state.generateSuccessor(index, action), depth, alpha, beta, (index + 1) % n)[0]
                    if value < min_value:
                        min_value = value
                        if min_value < alpha:
                            return min_value, " "
                        if beta > min_value:
                            beta = min_value
                return min_value, " "

        result = alpha_beta(gameState, 0, -99999999, 99999999, 0)
        return result[1]
        #util.raiseNotDefined()

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
        numb = gameState.getNumAgents()
        dep = self.depth        
        origin_move_ = "Stop"

        def expecti_max(state, depth=0, index=0, n=numb, depth_=dep, origin_move=origin_move_):
            if depth == depth_ or state.isWin() or state.isLose():
                return self.evaluationFunction(state),

            if index == 0:
                max_value = -999999.0
                move_ = origin_move
                for action in state.getLegalActions(0):
                    value = expecti_max(state.generateSuccessor(0, action), depth, (index + 1) % n)[0]
                    if value > max_value:
                        max_value = value
                        move_ = action

                return max_value, move_

            else:
                if index == n - 1:
                    depth += 1
                total = 0.0
                for action in state.getLegalActions(index):
                    value = expecti_max(state.generateSuccessor(index, action), depth, (index + 1) % n)[0]
                    total += float(value)
                average_value = total/float(len(state.getLegalActions(index)))
                return average_value, origin_move

        result = expecti_max(gameState)
        return result[1]
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    from math import sqrt
    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    sum_ = 0
    Food = Food.asList()

    ghost_distances = []
    if currentGameState.isLose():
        return -9999999
    if currentGameState.isWin():
        return 9999999

    for ghost_position in currentGameState.getGhostPositions():
        ghost_distances.append(manhattanDistance(Pos, ghost_position))
    min_ghost_distance = min(ghost_distances)
    min_ghost_distance = float(min_ghost_distance)
    danger = 0
    if currentGameState.hasWall(Pos[0], Pos[1]):
        return -999999999
    if min_ghost_distance < 2:
        danger -= 99999999

    total_food_distance = 0
    average_food_distance = 0
    food_distances = []
    if Food:
        for food_ in Food:
            total_food_distance += float(manhattanDistance(Pos, food_))
            food_distances.append(float(manhattanDistance(Pos, food_)))
        average_food_distance = total_food_distance / len(Food)

    min_food_distance = 0
    max_food_distance = 0
    if food_distances:
        min_food_distance += min(food_distances)
        max_food_distance += max(food_distances)
    else:
        return float('inf')

    big_dots = len(currentGameState.getCapsules())

    normal_ghosts = []
    scared_ghosts = []

    for ghost in currentGameState.getGhostStates():
        if ghost.scaredTimer:
            scared_ghosts.append(ghost)
        else:
            normal_ghosts.append(ghost)

    normal_ghost_distances = []
    scared_ghost_distances = []

    for ghost in normal_ghosts:
        normal_ghost_distances.append(manhattanDistance(Pos, ghost.getPosition()))
    for ghost in scared_ghosts:
        scared_ghost_distances.append(manhattanDistance(Pos, ghost.getPosition()))

    min_normal_ghost_distance = 0
    min_scared_ghost_distance = 0

    if normal_ghost_distances:
        min_normal_ghost_distance = min(normal_ghost_distances)

    min_normal_ghost_distance = max(min_normal_ghost_distance, 15)

    if scared_ghost_distances:
        min_scared_ghost_distance = min(scared_ghost_distances)
    else:
        min_scared_ghost_distance = 0

    food_amount = len(Food)
    score = currentGameState.getScore()
    sum_ = -200 * big_dots - 40 * food_amount + 0.99 * score - 2 * min_scared_ghost_distance \
           - 1.8 * min_food_distance - 2.0 / min_normal_ghost_distance + 1 * sqrt(max_food_distance)
    
    return sum_
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

