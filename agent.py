import random, re, datetime
import sys


class Agent(object):
    def __init__(self, game):
        self.game = game

    def getAction(self, state):
        raise Exception("Not implemented yet")


class RandomAgent(Agent):
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)


class SimpleGreedyAgent(Agent):
    # a one-step-lookahead greedy agent that returns action with max vertical advance
    def getAction(self, state):
        legal_actions = self.game.actions(state)

        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        if player == 1:
            max_vertical_advance_one_step = max([action[0][0] - action[1][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[0][0] - action[1][0] == max_vertical_advance_one_step]
        else:
            max_vertical_advance_one_step = max([action[1][0] - action[0][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[1][0] - action[0][0] == max_vertical_advance_one_step]
        self.action = random.choice(max_actions)


class GayGayMinimaxAgent(Agent):

    # a stupid evaluation function of minimax algorithm
    def evalFunc(self, state):
        board = state[1]
        me1 = board.getPlayerPiecePositions(state[0])
        opponent = board.getPlayerPiecePositions(3 - state[0])

        evaluate = 0
        for position in me1:
            evaluate += (20 - position[0])
        for oppo_position in opponent:
            evaluate -= (oppo_position[0])

        # penalty = 0
        # for row in range(1, board.piece_rows + 1):
        #     for col in range(1, board.getColNum(row) + 1):
        #         if board.board_status[(row, col)] == 1:
        #             penalty += 1
        #
        # bonus = 0
        # for row in range(board.size * 2 - board.piece_rows, board.size * 2):
        #     for col in range(1, board.getColNum(row) + 1):
        #         if board.board_status[(row, col)] == 2:
        #             bonus += 1
        #
        # evaluate += (bonus * 2 - penalty * 2)

        return evaluate

    """
    Minimax Algorithm for AI course
    Inputs
    state : current state that are going to deal with
    n : defines the depth of Minimax searching
    alpha : related to a-b pruning, refering to the alpha of this layer
    beta : refering to the beta of this layer
    Returns
    (value, action) : a tuple with information value and the action taken
    Related Functions
    Max_value(state, n, alpha, beta, action) deals with max layer
    Min_value(state, n, alpha, beta, action) deals with min layer
    """
    def Max_value(self, state, n, alpha, beta):
        if n==0:
            return self.evalFunc(state)

        value = sys.maxsize * -1
        best_action = None
        for action in self.game.actions(state):
            value = max(value, self.Min_value(self.game.succ(state, action), n-1, alpha, beta))
            if value >= beta:
                if n==2:
                    return value, action
                else:
                    return value
            if value > alpha:
                alpha = value
                best_action = action
            # alpha = max(alpha, value)
        if n==2:
            return value, best_action
        else:
            return value

    def Min_value(self, state, n, alpha, beta):
        if n==0:
            return self.evalFunc(state)

        value = sys.maxsize
        for action in self.game.actions(state):
            value = min(value, self.Max_value(self.game.succ(state, action), n-1, alpha, beta))
            if value <= alpha:
                return value
            beta = min(value, beta)
        return value

    def Minimax(self, state, n, alpha=sys.maxsize * -1, beta=sys.maxsize):
        value, action = self.Max_value(state, n, alpha, beta)
        return action

    # a minimax agent unknow what it is doing yet
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        # depth of minimax algorithm
        n = 2
        ### START CODE HERE ###
        best_action = self.Minimax(state, n)
        self.action = best_action
        ### END CODE HERE ###
