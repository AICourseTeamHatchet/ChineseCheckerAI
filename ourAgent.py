from util import *
from queue import PriorityQueue
from agent import Agent
import random

class GayGayMinimaxAgent(Agent):
    """
    This class implements the minimax algorithm, using alpha-beta pruning as well.
    """
    def late_game(self, agent_pos, opponent_pos):
        """
        This function is designed for evaluating the early game, contributing as a part of the
        whole evaluation function
        :param state: The current state
        :return: A value specifying the evaluation result
        """
        """
        # Another function that evaluates the late game
        terminate_state = [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (4, 4)]
        for checker in agent_pos:
            if checker in terminate_state:
                eval_value += 1
        return eval_value
        """
        eval_value = 0
        for pos_a in agent_pos:
            eval_value += (20 - pos_a[0])
        for pos_o in opponent_pos:
            eval_value -= pos_o[0]
        return eval_value

    def mid_game(self, agent_pos, opponent_pos):

        eval_value = 0
        # Calculate the sparsity of the distribution of checkers
        # We hope the checkers of one kind are close, and not too sparse from each other
        agent_sparsity_row = agent_pos[-1][0] - agent_pos[0][0]
        opponent_sparsity_row = opponent_pos[-1][0] - opponent_pos[0][0]
        eval_value = eval_value + (opponent_sparsity_row - agent_sparsity_row)

        # In this part, we take advantage of the opponent, using their checkers as well
        # This is evaluated by a rough L2 distance
        # Maybe too complicated
        """for i in range(10):
            l2_dis = math.sqrt((agent_pos[i][0] - opponent_pos[i][0]) ** 2 + (agent_pos[i][1] - opponent_pos[i][1]) ** 2)
            eval_value = eval_value + (19 - l2_dis)"""

        # We rather use the distance of columns
        for i in range(10):
            dis = abs(agent_pos[i][0] - opponent_pos[i][0])
            eval_value += dis

        return eval_value

    def early_game(self, agent_pos, opponent_pos):
        #opponent_pos = board.getPlayerPiecePositions(3 - state[0])
        # When in early game, a large probability is that our moves seldom depend on
        # the state of the opponent, we hope that checkers at the bottom moves out as fast
        # as possible
        eval_value = 0
        for pos in agent_pos:
            eval_value -= pos[0]


        return eval_value

    def h_function(self, agent_pos):
        """
        This function defines the heuristic function for the AStar algorithm
        :param: agent_pos: The position of the agent's checkers
        :return: h value.
        """
        terminal_state = [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (4, 4)]
        count = 0
        for p in agent_pos:
            if p in terminal_state:
                count -= 300
        if count == 0:
            count += 1000
        agent_pos.sort()
        for i in range (10):
            count += agent_pos[i][0]

        return count

    def AstarForEnding(self, state):
        """
        This function deals with the ending of the game, preventing the occurrence of some
        annoying conditions.
        :param agent_pos: The position of the agent's checkers
        :return: The path for the checkers. Stored in a list, each element with form (pos, adj_pos)
        """
        board = state[1]
        agent_pos = board.getPlayerPiecePositions(state[0])
        Astar_queue = PriorityQueue()
        final_path = []
        initial_h = 0
        count = 0
        while not player_win(agent_pos) and len(final_path) < 8:
            legal_actions = self.game.actions(state)
            for ac in legal_actions:
                count += 1
                new_final_path = copy.copy(final_path)
                new_state = self.game.succ(state, ac)
                new_state_tuple = (3 - new_state[0], new_state[1])
                new_board = new_state_tuple[1]
                new_agent_pos = new_board.getPlayerPiecePositions(new_state_tuple[0])
                #print (ac, agent_pos, new_agent_pos)
                from_pos = [p for p in agent_pos if p not in new_agent_pos][0]
                to_pos = [p for p in new_agent_pos if p not in agent_pos][0]
                #print (from_pos, to_pos)
                new_final_path.append((from_pos, to_pos))
                Astar_queue.put((initial_h + self.h_function(new_agent_pos), new_final_path, count, new_state_tuple))
            initial_h, final_path, _, state = Astar_queue.get()
            board = state[1]
            agent_pos = board.getPlayerPiecePositions(state[0])
            print (final_path)

        return final_path[0]

    def eval_func(self, state):
        evaluate = 0
        board = state[1]
        agent_pos = board.getPlayerPiecePositions(state[0])
        opponent_pos = board.getPlayerPiecePositions(3 - state[0])
        agent_pos.sort()
        opponent_pos.sort()
        #print(self.early_game(agent_pos, opponent_pos), self.mid_game(agent_pos, opponent_pos),
        #      self.late_game(agent_pos, opponent_pos))

        alpha = 0
        beta = 1
        gamma = 100
        #print(agent_pos)

        evaluate += alpha * self.early_game(agent_pos, opponent_pos) + beta * self.mid_game(agent_pos, opponent_pos) + \
                    gamma * self.late_game(agent_pos, opponent_pos)
        #print (evaluate)

        return evaluate

    def feature_eval(self, state):
        evaluate = 0
        player = state[0]
        board = state[1]
        agent_pos = board.getPlayerPiecePositions(state[0])
        opponent_pos = board.getPlayerPiecePositions(3 - state[0])
        agent_pos.sort()
        opponent_pos.sort()

        """
        Distances to win for both of us
        """
        myDistanceWin = vertical_distance(agent_pos, player)
        herDistanceWin = vertical_distance(opponent_pos, 3 - player)

        """
        Distances to the center of the puzzle
        """
        myDistanceCenter = midline_distance(agent_pos, state[1])
        # herDistanceCenter = midline_distance(opponent_pos)

        """
        Moving distances summing up
        """
        actions = self.game.actions(state)
        last = actions[0][0]
        f = {}
        stepping = 0
        for action in actions:
            if action[0] in f.keys():
                f[action[0]].append(action[0][0] - action[1][0])
            else:
                f[action[0]] = []
                f[action[0]].append(action[0][0] - action[1][0])

        for i in f.keys():
            stepping += max(f[i])
        # stepping = sum([action[0][0] - action[1][0] for action in actions])

        evaluate = 1.7 * (myDistanceWin - herDistanceWin) + 0.14 * (-myDistanceCenter) + 0.5 * stepping
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
            return self.feature_eval(state)

        value = sys.maxsize * -1
        best_action = None

        actions = self.game.actions(state)
        actions.sort(key=self.takeDepth)
        for action in actions:
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
        if n == 0:
            return self.feature_eval(state)

        value = sys.maxsize
        actions = self.game.actions(state)
        actions.sort(key=self.takeDepth)
        actions = actions[::-1]
        for action in actions:
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
            return self.feature_eval(state)

        value = sys.maxsize * -1
        best_action = None

        actions = self.game.actions(state)
        actions.sort(key=self.takeDepth)
        for action in actions:
            next_value = self.maximax_value(self.game.succ(state, action), n-1)
            if value < next_value:
                value = next_value
                best_action = action

        if n == 2:
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
            max_vertical_advance_one_step = max([action[0][0] - action[1][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[0][0] - action[1][0] == max_vertical_advance_one_step]
            self.action = random.choice(max_actions)
        else:
            print ("max")
            best_action = self.maximax(state, n)

        if best_action == None:
            print ("random")
            pass
        else:
            self.action = best_action
        print (self.action)

        ### END CODE HERE ###
