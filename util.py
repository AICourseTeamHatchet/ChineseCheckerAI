"""
A file consisting all kinds of utilities
Such as heuristic functions, evaluation functions
To be Continued
"""

import random, re, datetime
import sys
import math

# get the first and last element based on position and player
def getFirstLastElement(agent_pos, player):
    if player == 1:
        first = agent_pos[0][0]
        last = agent_pos[0][0]
        for position in agent_pos:
            if position[0] < first:
                first = position[0]
            if position[0] > last:
                last = position[0]
    else:
        first = agent_pos[0][0]
        last = agent_pos[0][0]
        for position in agent_pos:
            if position[0] > first:
                first = position[0]
            if position[0] < last:
                last = position[0]

    return first, last

# is the game starting battle with each other now
def isBattle(MyFirst, HerFirst, player):
    if player == 2:
        return (MyFirst - HerFirst >= 2)
    else:
        return (HerFirst - MyFirst >= 2)

# is the game going to the end of the state now
def isEnding(MyLast, HerLast, player, k = 0):
    if player == 1:
        return (MyLast + k <= HerLast)
    else:
        return (HerLast + k <= MyLast)

# getting vertical distance to goal state sum
def vertical_distance(agent_pos, player):
    distance = 0

    if player == 1:
        for position in agent_pos:
            distance += 20 - position[0]
    else:
        for position in agent_pos:
            distance += position[0]

    return distance

# getting the distance from all the nodes to the mid column line
def midline_distance(agent_pos, board):
    distance = 0

    for position in agent_pos:
        distance += abs(position[1] - board.getColNum(position[0]) / 2)

    return distance

# check if the chesses are too loose
def check_looseness(agent_pos):
    distance = 0
    average = 0

    for position in agent_pos:
        average += position[0] / 10
    for position in agent_pos:
        distance += abs(position[0] - average)

    return distance

# Check whether the player has reached the terminal state(actually not the same with the isEnd() function)
# This is a bool function
def player_win(agent_pos):
    terminal_state = [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (4, 4)]
    for p in agent_pos:
        if p not in terminal_state:
            return False
    return True
