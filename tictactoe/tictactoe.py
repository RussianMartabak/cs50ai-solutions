"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math
from shutil import ExecError

X = "X"
O = "O"
EMPTY = None


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
        for j in range(len(i)):
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
            step = 0
            if i == 0 and j == 0 or j == 2:
                diagonalEdge = board[i][j]
                if j == 0:
                    step = 1
                else:
                    step = -1
                #for loop but the step depends on a variable
                
    
    #check if h/v/d is 3 then return winner
    

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    state = countItem(board)
    if state["EMPTY"] == 0:
        return True
    else:
        return False
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
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
class IlegalMoveError(Exception):
    pass
