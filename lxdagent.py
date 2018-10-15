import random, re, datetime


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
        

class FODMinimaxAgent(Agent):
    def evaluation(self, state):
        end, winner = state[1].isEnd(100)
        if end:     # current board is an ending board
            if winner == 1:
                return 100
            return -100
        value = 0
        for player in range(1, 3):
            pos = state[1].getPlayerPiecePositions(player)
            for x, y in pos:
                value += 10 - x
        return value


    def minimaxValue(self, state, alpha, beta, d, max_d, player):    # d:depth, max_d:max depth
        if d == max_d:
            return self.evaluation(state)
        if player == 1:
            value = -100
            legal_actions = self.game.actions(state)
            random.shuffle(legal_actions)
            for action in legal_actions:
                value = max(value, self.minimaxValue(self.game.succ(state, action), alpha, beta, d+1, max_d, 2))
                if value > beta:
                    return value
                alpha = max(alpha, value)
            return value
        else:
            value = 100
            legal_actions = self.game.actions(state)
            random.shuffle(legal_actions)
            for action in legal_actions:
                value = min(value, self.minimaxValue(self.game.succ(state, action), alpha, beta, d+1, max_d, 1))
                if value < alpha:
                    return value
                beta = min(beta, value)
            return value


    def getAction(self, state):
        legal_actions = self.game.actions(state)
        random.shuffle(legal_actions)
        # self.action = random.choice(legal_actions)

        player = self.game.player(state)
        ### START CODE HERE ###

        if player == 1:
            value = -100
            for action in legal_actions:
                v = self.minimaxValue(self.game.succ(state, action), -100, 100, 1, 2, 2)
                if v > value:
                    value = v
                    self.action = action
        else:
            value = 100
            for action in legal_actions:
                v = self.minimaxValue(self.game.succ(state, action), -100, 100, 1, 2, 1)
                if v < value:
                    value = v
                    self.action = action 






        ### END CODE HERE ###



