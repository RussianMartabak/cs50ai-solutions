"""
Tic Tac Toe Player
"""

import math

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
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
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

