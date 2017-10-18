import pprint
import copy


# Sudoku board
# y -------->
#[[00, 01, 02, 03, 04, 05, 06, 07, 08],  x
#[10, 11, 12, 13, 14, 15, 16, 17, 18],   |
#[20, 21, 22, 23, 24, 25, 26, 27, 28],   |
#[30, 31, 32, 33, 34, 35, 36, 37, 38],   |
#[40, 41, 42, 43, 44, 45, 46, 47, 48],     
#[50, 51, 52, 53, 54, 55, 56, 57, 58],
#[60, 61, 62, 63, 64, 65, 66, 67, 68],
#[70, 71, 72, 73, 74, 75, 76, 77, 78],
#[80, 81, 82, 83, 84, 85, 86, 87, 88]]


sudokuBoard = []
variables = {}
domain = (1,2,3,4,5,6,7,8,9)

# Contains the blocks and their beginning and ending points
blocks = {1: ((0,0), (2,2)), 2: ((0,3), (2,5)), 3: ((0,6), (2,8)),
          4: ((3,0), (5,2)), 5: ((3,3), (5,5)), 6: ((3,6), (5,8)),
          7: ((6,0), (8,2)), 8: ((6,3), (8,5)), 9: ((6,6), (8,8))}


class treeNode(object):

    def __init__(self, board):
        self.board = copy.deepcopy(board)
        self.variables = {}
        


class sudokuVariable(object):
    
    def __init__(self, coords, block):
        self.remainingValues = []
        self.coords = coords
        self.block = block


def main():
    pass


# Given a board state initialize all of the variables and their domains
def initializeVariables(boardState):
    pass

# Checks row for constraint, returns possible values
def checkRow(variable, board):
    global domain
    values = []

    for i in range (0,9):
        if board[variable.coords[0]][i] != ' ':
            values.append(board[variable.coords[0]][i])

    return list(set(domain).difference(values))
        
    

# Checks column for constraints, returns possible values
def checkCol(variable, board):
    global domain
    values = []

    for i in range (0,9):
        if board[variable.coords[i]][0] != ' ':
            values.append(board[variable.coords[i]][0])

    return list(set(domain).difference(values))

# Checks 3X3 block for constraints, returns possible values, ASSUMES given variable is not already assigned a value
def check3by3(variable, board):
    global domain, blocks
    values = []

    block = variable.block

    blockCoords = blocks[block]

    for i in range(blockCoords[0][0], blockCoords[0][1] + 1):
        for j in range(blockCoords[1][0], blockCoords[1][1] + 1):
            if board[variable.coords[i]][j] != ' ':
                values.append(board[variable.coords[i]][j])

    return list(set(domain).difference(values))

# Given a variable and the current board find all of the constraints on it
def checkConstraints(variable, board):
    pass

def mrv():
    pass

def degree():
    pass

def forwardChecking():
    pass


# Call Main
main()