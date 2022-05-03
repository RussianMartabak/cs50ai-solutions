"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math
from shutil import ExecError

X = "X"
O = "O"
EMPTY = None
explorations = 0

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    #at start its X first
    cellCount = countItem(board=board)
    if cellCount["EMPTY"] == 9:
        return X
    # because X is first if their number is same its X turn
    elif cellCount["X"] == cellCount["O"]:
        return X
    else:
        return O

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    # i is row, j is column
    # basically just get all empty cells
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #take (row, column) as input
    row = action[0]
    column = action[1]
    result = deepcopy(board)
    playerItem = player(board)

    #check
    if board[row][column] != EMPTY:
        raise IlegalMoveError("Ilegal Move")
    result[row][column] = playerItem

    return result
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    vertical = 0
    horizontal = 0
    diagonal = 0
    
    #loop through all the board
    for i in range(len(board)):
        horizontal = 0
        #check by counting the number of edge item in horizontal line
        horizontalEdge = board[i][0]
        for j in range(len(board[i])):
            if board[i][j] == horizontalEdge:
                horizontal += 1
            
            else:
                horizontal = 0
            if horizontal == 3 and horizontalEdge != None:
                return horizontalEdge
            #count to down if now row is 0
            vertical = 0
            verticalEdge = board[i][j]
            if i == 0:
                for row in range(len(board)):
                    if board[row][j] == verticalEdge and verticalEdge != None:
                        vertical += 1
                    else:
                        vertical = 0
                    if vertical == 3:
                        return verticalEdge
            #go diagonal if its now at 0,0 or 0,3
            diagonal = 0
            stepj = 0
            if i == 0: 
                if j == 0 or j == 2:
                    diagonalEdge = board[i][j]
                    if j == 0:
                        stepj = 1
                    else:
                        stepj = -1
                    #for loop but the step depends on a variable
                    #k denote the iteration, will use it to modify both row and columns
                    # in diagonal movement both row and column is decreased with same value but 
                    # can be in one side a subtraction the other opposite
                    # in this loop we go from 0 to 2 (included)
                    # i should always start at zero so I just use the number here
                    for k in range(0, len(board)):
                        modifierj = stepj * k
                       
                        if board[0 + k][j + modifierj] == diagonalEdge:
                            diagonal += 1
                        if diagonal == 3:
                            return diagonalEdge
    return None

                    

    
    #check if h/v/d is 3 then return winner
    

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    state = countItem(board)
    if state["EMPTY"] == 0 or winner(board) is not None:
        return True
    else:
        return False
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    finalWinner = winner(board)
    if finalWinner == X:
        return 1
    elif finalWinner == O:
        return -1
    else:
        return 0
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #return (i, j)
    #probably need to make subfunctions for picking the worst value or the best value
    #poll action, get player
    possibleActions = actions(board)
    activePlayer = player(board)
    bestValue = None
    if activePlayer == X:
        bestValue = -2
    else:
        bestValue = 2
    best = None
    # generate max/min value of actions and pick an action that suit the AI personality
    decisions = [] #list of dictionary of decisions and its value
    for action in possibleActions:
        if activePlayer == X:
            
            decisionValue = maxValue(action, board)
            if decisionValue > bestValue:
                bestValue = decisionValue
            dict = {
                "value" : decisionValue,
                "action" : action
            }
            decisions.append(dict)
        else:
            decisionValue = minValue(action, board)
            if decisionValue < bestValue:
                bestValue = decisionValue
            dict = {
                "value" : decisionValue,
                "action" : action
            }
            decisions.append(dict)

    #pick 
    for item in decisions:
        if item["value"] == bestValue:
            #print('explored:', explorations)
            return item["action"]

    raise NotImplementedError

#function to count board cells for items
#return dictionary
def countItem(board):
    count = {
        "X": 0,
        "O": 0,
        "EMPTY": 0
    }
    for row in board:
        for cell in row:
            if cell == X:
                count["X"] += 1
            elif cell == O:
                count["O"] += 1
            elif cell == EMPTY:
                count["EMPTY"] += 1
            
    return count

#take action (i, j) and return the max value
def maxValue(action, board):
    #base state
    #global explorations 
    #explorations += 1
    currentBoard = deepcopy(board)
    afterBoard = result(currentBoard, action)
    if terminal(afterBoard):
        return utility(afterBoard)
    #recursive state
    #generate multiple decisions
    possibilities = actions(afterBoard)
    #consider each by getting the value from min player
    max = -2
    #get what value would a min player give to the board
    for action in possibilities:
        decisionValue = minValue(action, afterBoard)
        if decisionValue > max:
            max = decisionValue

        
    return max

def minValue(action, board):
    #base state
    #global explorations
    #explorations += 1
    currentBoard = deepcopy(board)
    afterBoard = result(currentBoard, action)
    if terminal(afterBoard):
        return utility(afterBoard)
    #recursive state
    #generate multiple decisions
    possibilities = actions(afterBoard)
    #consider each by getting the value from max player
    min = 2
    
    for action in possibilities:
        decisionValue = maxValue(action, afterBoard)
        if decisionValue < min:
            min = decisionValue
        
    return min

class IlegalMoveError(Exception):
    pass
