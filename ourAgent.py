from util import *
from queue import PriorityQueue
from agent import Agent
import random

class GayGayMinimaxAgent(Agent):
    """
    This class implements the minimax algorithm, using alpha-beta pruning as well.
    """

    def feature_prune(self, state1, state2):
        evaluate = 0
        board1 = state1[1]
        board2 = state2[1]
        pos1 = board1.getPlayerPiecePositions(state2[0])
        pos2 = board2.getPlayerPiecePositions(state2[0])

        for position1 in pos1:
            evaluate += position1[0]
        for position2 in pos2:
            evaluate -= position2[0]

        return evaluate * 40.65

    def simpleEvaluate(self, state):
        player = state[0]
        board = state[1]
        agent_pos = board.getPlayerPiecePositions(state[0])

        myDistanceWin = 0
        for position in agent_pos:
            if player == 1:
                myDistanceWin += 20 - position[0]
            else:
                myDistanceWin += position[0]

        return myDistanceWin

    def feature_eval2(self, state):
        evaluate = 0
        player = state[0]
        board = state[1]
        agent_pos = board.getPlayerPiecePositions(state[0])
        opponent_pos = board.getPlayerPiecePositions(3 - state[0])

        myDistanceWin = 0
        herDistanceWin = 0
        myDistanceCenter = 0
        average_row = 0
        myLooseness = 0
        rightsideness = 0

        for position in agent_pos:
            myDistanceWin += position[0]
            myDistanceCenter += abs(position[1] - board.getColNum(position[0]) / 2)
            average_row += position[0] / 10.0

        for position in opponent_pos:
            herDistanceWin += 20 - position[0]

        for position in agent_pos:
            myLooseness += abs(position[0] - average_row)

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
                    f[action[0]] = (action[0][0] - action[1][0])
            else:
                f[action[0]] = (action[0][0] - action[1][0])

        for i in f.keys():
            stepping += f[i]
        stepping = -stepping
        print ("stepping", stepping, " myLooseness", myLooseness, " mhdis", (myDistanceWin - herDistanceWin))
        # stepping = sum([action[0][0] - action[1][0] for action in actions])

        evaluate = 2.1 * (myDistanceWin - herDistanceWin) + 0.34 * (-myDistanceCenter) + 0.7 * stepping - 0.35 * myLooseness
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
            average += position[0] / 10.0

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
        # print (myLooseness)
        evaluate = 2.1 * (myDistanceWin - herDistanceWin) + 0.34 * (-myDistanceCenter) + 0.7 * stepping - 0.35 * myLooseness
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
            if state[0] == 1:
                if value > 0:
                    value = max(value, self.min_value(self.game.succ(state, action), n-1, alpha, beta) / (0.06 * (21 - action[0][0])))
                else:
                    value = max(value, self.min_value(self.game.succ(state, action), n-1, alpha, beta) * (0.06 * (21 - action[0][0])))
            else:
                if value < 0:
                    value = max(value, self.min_value(self.game.succ(state, action), n-1, alpha, beta) * ((0.06 * action[0][0])))
                else:
                    value = max(value, self.min_value(self.game.succ(state, action), n-1, alpha, beta) / ((0.06 * action[0][0])))
            if value >= beta:
                if n == 2:
                    return value, action
                else:
                    return value
            if value > alpha:
                alpha = value
                if n == 2:
                    self.action = action
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
            successor = self.game.succ(state, action)
            if state[0] == 2:
                if self.feature_prune(successor, state) <= 65:
                    continue
            # else:
            #     if self.feature_prune(successor, state) <= -40:
            #         continue
            value = min(value, self.max_value(successor, n-1, alpha, beta))
            # print (value)
            # print (value)
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
        # print (self.action)

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
            # best_action = self.minimaxEnd(state, n)
            end_of_end = self.enumerate_ending(state, player)
            if end_of_end == -1:
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
        # print (self.action)

    def enumerate_ending(self ,state, player):
        """
        This function deals with the ending state, when greedy meets its boudaries;
        """
        conditions_player_1 = [[(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (5, 1)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 4), (5, 1)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 3), (4, 4), (5, 1)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 2), (4, 3), (4, 4), (5, 5)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 3), (4, 4), (5, 5)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 4), (5, 5)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (5, 2)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 4), (5, 2)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 2), (4, 3), (4, 4), (5, 4)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 3), (4, 4), (5, 4)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 2), (4, 3), (4, 4), (5, 3)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (5, 3)]]

        conditions_player_2 = [[(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 1), (16, 2), (16, 3), (15, 1)], # 0
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 1), (16, 3), (16, 4), (15, 1)], # 1
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 1), (16, 2), (16, 4), (15, 1)], # 2
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 2), (16, 3), (16, 4), (15, 5)], # 3
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 1), (16, 3), (16, 4), (15, 5)], # 4
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 1), (16, 2), (16, 4), (15, 5)], # 5
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 1), (16, 2), (16, 3), (15, 2)], # 6
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 1), (16, 2), (16, 4), (15, 2)], # 7
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 2), (16, 3), (16, 4), (15, 4)], # 8
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 1), (16, 3), (16, 4), (15, 4)], # 9
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 2), (16, 3), (16, 4), (15, 3)], # 10
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 1), (16, 2), (16, 3), (15, 3)]] # 11
        board = state[1]
        agent_pos = board.getPlayerPiecePositions(player)
        index = -1
        if player == 1:
            for i in range(len(conditions_player_1)):
                if conditions_player_1[i] == agent_pos:
                    index = i
                    break
            if index == 0:
                self.action = ((4, 2), (4, 4))
            elif index == 1:
                self.action = ((4, 1), (4, 3))
            elif index == 2:
                self.action = ((4, 1), (4, 2))
            elif index == 3:
                self.action = ((4, 3), (4, 1))
            elif index == 4:
                self.action = ((4, 4), (4, 2))
            elif index == 5:
                self.action = ((4, 4), (4, 3))
            elif index == 6:
                self.action = ((4, 2), (4, 4))
            elif index == 7:
                self.action = ((4, 2), (4, 3))
            elif index == 8:
                self.action = ((4, 3), (4, 1))
            elif index == 9:
                self.action = ((4, 3), (4, 2))
            elif index == 10:
                self.action = ((4, 2), (4, 1))
            elif index == 11:
                self.action = ((4, 3), (4, 4))
        else:
            for i in range(len(conditions_player_2)):
                if conditions_player_2[i] == agent_pos:
                    index = i
                    break
            if index == 0:
                self.action = ((16, 2), (16, 4))
            elif index == 1:
                self.action = ((16, 1), (16, 2))
            elif index == 2:
                self.action = ((16, 1), (16, 3))
            elif index == 3:
                self.action = ((16, 3), (16, 1))
            elif index == 4:
                self.action = ((16, 4), (16, 2))
            elif index == 5:
                self.action = ((16, 4), (16, 3))
            elif index == 6:
                self.action = ((16, 2), (16, 4))
            elif index == 7:
                self.action = ((16, 2), (16, 3))
            elif index == 8:
                self.action = ((16, 3), (16, 1))
            elif index == 9:
                self.action = ((16, 3), (16, 2))
            elif index == 10:
                self.action = ((16, 2), (16, 1))
            elif index == 11:
                self.action = ((16, 3), (16, 4))
        return index

        ### END CODE HERE ###
