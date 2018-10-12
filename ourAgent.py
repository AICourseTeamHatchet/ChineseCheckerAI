from util import *
from queue import PriorityQueue
from agent import Agent
import random

class GayGayMinimaxAgent(Agent):
    """
    This class implements the minimax algorithm, using alpha-beta pruning as well.
    """

    def feature_eval2(self, state):
        evaluate = 0
        player = state[0]
        board = state[1]
        agent_pos = board.getPlayerPiecePositions(state[0])
        opponent_pos = board.getPlayerPiecePositions(3 - state[0])

        myDistanceWin = 0
        herDistanceWin = 0
        myDistanceCenter = 0
        average = 0
        myLooseness = 0

        for position in agent_pos:
            myDistanceWin += position[0]
            myDistanceCenter += abs(position[1] - board.getColNum(position[0]) / 2)
            average += position[0] / 10

        for position in opponent_pos:
            herDistanceWin += 20 - position[0]

        for position in agent_pos:
            myLooseness += abs(position[0] - average)

        """
        Moving distances summing up
        """
        actions = self.game.actions(state)
        last = actions[0][0]
        f = {}
        stepping = 0

        for action in actions:
            if action[0] in f.keys():
                if (action[0][0] - action[1][0]) < f[action[0]]:
                    f[action[0]] = action[0][0] - action[1][0]
            else:
                f[action[0]] = action[0][0] - action[1][0]

        for i in f.keys():
            stepping += f[i]
        stepping = -stepping

        # stepping = sum([action[0][0] - action[1][0] for action in actions])

        evaluate = 1.7 * (myDistanceWin - herDistanceWin) + 0.14 * (-myDistanceCenter) + 0.5 * stepping - 0.3 * myLooseness
        return evaluate

    def feature_eval1(self, state):
        evaluate = 0
        player = state[0]
        board = state[1]
        agent_pos = board.getPlayerPiecePositions(state[0])
        opponent_pos = board.getPlayerPiecePositions(3 - state[0])

        myDistanceWin = 0
        herDistanceWin = 0
        myDistanceCenter = 0
        average = 0
        myLooseness = 0

        for position in agent_pos:
            myDistanceWin += 20 - position[0]
            myDistanceCenter += abs(position[1] - board.getColNum(position[0]) / 2)
            average += position[0] / 10

        for position in opponent_pos:
            herDistanceWin += position[0]

        for position in agent_pos:
            myLooseness += abs(position[0] - average)

        """
        Moving distances summing up
        """
        actions = self.game.actions(state)
        last = actions[0][0]
        f = {}
        stepping = 0

        for action in actions:
            if action[0] in f.keys():
                if (action[0][0] - action[1][0]) > f[action[0]]:
                    f[action[0]] = action[0][0] - action[1][0]
            else:
                f[action[0]] = action[0][0] - action[1][0]

        for i in f.keys():
            stepping += f[i]

        # stepping = sum([action[0][0] - action[1][0] for action in actions])

        evaluate = 1.7 * (myDistanceWin - herDistanceWin) + 0.14 * (-myDistanceCenter) + 0.5 * stepping - 0.3 * myLooseness
        return evaluate

    # Used for minimax pruning
    def takeDepth(self, action):
        return action[1][0] - action[0][0]

    def max_value(self, state, n, alpha, beta):
        """
        This function determines the maximum value for the current state.
        :param state: Current state for evaluating
        :param n: The depth for minimax search
        :param alpha: Parameter of the alpha-beta pruning, the smaller value
        :param beta: Parameter of the alpha-beta pruning, the larger value
        :return: The result value for the state
        """
        if n == 0:
            if state[0] == 1:
                return self.feature_eval1(state)
            else:
                return self.feature_eval2(state)

        value = sys.maxsize * -1
        best_action = None

        actions = self.game.actions(state)
        if state[0] == 1:
            actions.sort(key=self.takeDepth)
        else:
            actions.sort(key=self.takeDepth)
            actions = actions[::-1]
        for action in actions:
            if state[0] == 1:
                if action[0][0] - action[1][0] < -1:
                    continue
                if action[0][0] <= 4:
                    continue
            else:
                if action[0][0] - action[1][0] > 1:
                    continue
                if action[0][0] >= 16:
                    continue
            value = max(value, self.min_value(self.game.succ(state, action), n-1, alpha, beta))
            if value >= beta:
                if n == 2:
                    return value, action
                else:
                    return value
            if value > alpha:
                alpha = value
                best_action = action
        if n == 2:
            return value, best_action
        else:
            return value


    def min_value(self, state, n, alpha, beta):
        """
        This function determines the minimum value for the current state
        :param state: :)
        :param n: :)
        :param alpha: :)
        :param beta: :)
        :return: :)
        """

        value = sys.maxsize
        actions = self.game.actions(state)
        if state[0] == 2:
            actions.sort(key=self.takeDepth)
            actions = actions[::-1]
        else:
            actions.sort(key=self.takeDepth)
        for action in actions:
            if state[0] == 2:
                if action[0][0] - action[1][0] > 1:
                    continue
                if action[0][0] >= 16:
                    continue
            else:
                if action[0][0] - action[1][0] < -1:
                    continue
                if action[0][0] <= 4:
                    continue
            value = min(value, self.max_value(self.game.succ(state, action), n-1, alpha, beta))
            if value <= alpha:
                return value
            beta = min(value, beta)
        return value


    def minimax(self, state, n, alpha = sys.maxsize * -1, beta = sys.maxsize):
        value, action = self.max_value(state, n, alpha, beta)
        return action

    """
    Function calculating maximax
    maybe used at the beginning of the game
    inputs
    state : u know, the current state of the puzzle
    n : recursion depth
    outputs
    value / action : the value evaluated by the eval_func, and the action may be taken
    """
    def maximax_value(self, state, n):
        if n == 0:
            if state[0] == 1:
                return self.feature_eval1(state)
            else:
                return self.feature_eval2(state)

        value = sys.maxsize * -1
        best_action = None

        actions = self.game.actions(state)
        if state[0] == 1:
            actions.sort(key=self.takeDepth)
        else:
            actions.sort(key=self.takeDepth)
            actions = actions[::-1]
        for action in actions:
            next_value = self.maximax_value((state[0], self.game.succ(state, action)[1]), n-1)
            if value < next_value:
                value = next_value
                best_action = action

        if n == 1:
            return value, best_action
        else:
            return value

    def maximax(self, state, n):
        value, action = self.maximax_value(state, n)
        return action

    def getAction(self, state):
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)
        print (self.action)

        player = self.game.player(state)
        n = 2 # Referring to the depth
        ### START CODE HERE ###
        best_action = None
        agent_pos = state[1].getPlayerPiecePositions(player)
        opponent_pos = state[1].getPlayerPiecePositions(3 - player)
        myFirst, myLast = getFirstLastElement(agent_pos, player)
        herFirst, herLast = getFirstLastElement(opponent_pos, 3 - player)

        if isBattle(myFirst, herFirst, player) and not isEnding(myLast, herLast, player):
            print ("min")
            best_action = self.minimax(state, n)
        elif isEnding(myLast, herLast, player):
            if player == 1:
                max_vertical_advance_one_step = max([action[0][0] - action[1][0] for action in legal_actions])
                max_actions = [action for action in legal_actions if
                               action[0][0] - action[1][0] == max_vertical_advance_one_step]
            else:
                max_vertical_advance_one_step = max([action[1][0] - action[0][0] for action in legal_actions])
                max_actions = [action for action in legal_actions if
                               action[1][0] - action[0][0] == max_vertical_advance_one_step]
            self.action = random.choice(max_actions)
        else:
            print ("max")
            best_action = self.maximax(state, 1)

        if best_action == None:
            print ("random")
            pass
        else:
            self.action = best_action
        print (self.action)

        ### END CODE HERE ###
