# Authors
#   Luke Mammen
#   Morgan Knoch

import copy
import heapq

# sudokuBoard[row][column]
sudokuBoard1 = [[' ',' ','1',   ' ',' ','2',   ' ',' ',' '],
               [' ',' ','5',   ' ',' ','6',   ' ','3',' '],
               ['4','6',' ',   ' ',' ','5',   ' ',' ',' '],

               [' ',' ',' ',   '1',' ','4',   ' ',' ',' '],
               ['6',' ',' ',   '8',' ',' ',   '1','4','3'],
               [' ',' ',' ',   ' ','9',' ',   '5',' ','8'],

               ['8',' ',' ',   ' ','4','9',   ' ','5',' '],
               ['1',' ',' ',   '3','2',' ',   ' ',' ',' '],
               [' ',' ','9',   ' ',' ',' ',   '3',' ',' ']]

# the starting domain for each variable
domain = ('1','2','3','4','5','6','7','8','9')

# Contains the blocks and their beginning and ending points
blocks = {1: ((0,0), (2,2)), 2: ((0,3), (2,5)), 3: ((0,6), (2,8)),
          4: ((3,0), (5,2)), 5: ((3,3), (5,5)), 6: ((3,6), (5,8)),
          7: ((6,0), (8,2)), 8: ((6,3), (8,5)), 9: ((6,6), (8,8))}


# The current state of the game board
class boardState(object):
    def __init__(self, board):
        self.board = copy.deepcopy(board)
        self.variables = []     # min-heap ordered by MRV then Degree heuristic
        self.updateVars()

    def updateVars(self):
        self.variables = []

        for row in range(9):
            for col in range(9):
                if self.board[row][col] == ' ':
                    heapq.heappush( self.variables, sudokuVariable( (row,col), self.board ) )
# boardState(object)
        
  
# defines each square on the board
class sudokuVariable(object):
    def __init__(self, coords, board):
        self.board = board
        self.remainingValues = []
        self.coords = coords    # (row,col)
        self.block = getBlock(coords)
        checkConstraints(self, self.board)
        self.mrv = len(self.remainingValues)
        self.degree = getDegree(self)

    # less than comparator.
    def __lt__(self, other):
        # if mrv's are same, break tie with degree.
        if self.mrv == other.mrv:
            return self.degree >= other.degree # greeater than; bigger degree is better.
        else:
            return self.mrv < other.mrv
# sudokuVariable(object)


def main():
    board = boardState(sudokuBoard1)
    printBoard(board.board)
    backTrackingSearch( board )
    printBoard(board.board)
# main()


# Perform backtracking search on the sudoku puzzle
def backTrackingSearch( boardState ):
    if isComplete( boardState ):
        return True

    var = heapq.heappop( boardState.variables )

    for value in var.remainingValues:
        makeMove(var, boardState)

        if backTrackingSearch( boardState ):
            return True

        heapq.heappush( boardState.variables, var )
        undoMove(var, boardState)

    return False
# backTrackingSearch()


# make move on sudoku puzzle
def makeMove(var, boardState):
    boardState.board[var.coords[0]][var.coords[1]] = var.remainingValues[0]
    boardState.updateVars()
# makeMove()


# undo move on sodoku puzzle
def undoMove(var, boardState):
    boardState.board[var.coords[0]][var.coords[1]] = ' '
    boardState.updateVars()
# undoMove()


# checks board for empty spaces
def isComplete( boardState ):
    for row in range(9):
        for col in range(9):
            if boardState.board[row][col] == ' ':
                return False

    return True
# isComplete()


# calculate the degree for a given variable
def getDegree(var):
    degree = 0

    # check column
    for row in range(9):
        if row != var.coords[0] and var.board[row][var.coords[1]] == ' ':
            degree += 1

    # check row
    for col in range(9):
        if col != var.coords[1] and var.board[var.coords[0]][col] == ' ':
            degree += 1

    # check block
    block = var.block      # get start and end coords for local block
    blockCoords = blocks[block]
    s_row = blockCoords[0][0]
    s_col = blockCoords[0][1]
    e_row = blockCoords[1][0]
    e_col = blockCoords[1][1]

    for row in range( s_row, e_row + 1 ):
        for col in range( s_col, e_col + 1 ):
            if row != var.coords[0] and col != var.coords[1] and var.board[row][col] == ' ':
                degree += 1

    return degree
# getDegree()


# calculate the block the given coords are in
def getBlock(coords):
    return ( ( coords[1]//3 ) + 1 ) + ( 3 * (coords[0]//3) )
# getBlock()


# Given a variable and the current board find all of the constraints on it
def checkConstraints(variable, board):
    row_con = checkRow( variable, board )
    col_con = checkCol( variable, board )
    blc_con = check3by3( variable, board )

    final_con = set(blc_con) & set(row_con) & set(col_con) # takes the intersection

    variable.remainingValues = list( final_con )
# checkConstraints()


# Checks row for constraint, returns possible values
def checkRow(variable, board):
    global domain   
    values = []                 # list of values "variable" CANNOT be.
    row = variable.coords[0]    # the row "variable" is in.

    for i in range (0,9):
        if board[row][i] != ' ':
            values.append(board[row][i])

    return list(set(domain).difference(values)) # list of values "variable" CAN be. 
# checkRow()
  

# Checks column for constraints, returns possible values
def checkCol(variable, board):
    global domain
    values = []                 # list of values "variable" cannot be.
    col = variable.coords[1]    # the column "variable" is in.

    for i in range (0,9):
        if board[i][col] != ' ':
            values.append(board[i][col])

    return list(set(domain).difference(values)) # list of values "variable" CAN be.
# checkCol()


# Checks 3X3 block for constraints, returns possible values, ASSUMES given variable is not already assigned a value
def check3by3(variable, board):
    global domain, blocks
    values = []                 # list of values "variable" cannot be.

    block = variable.block      # get start and end coords for local block
    blockCoords = blocks[block]
    s_row = blockCoords[0][0]
    s_col = blockCoords[0][1]
    e_row = blockCoords[1][0]
    e_col = blockCoords[1][1]

    # check local block for valid values for 'variable'.
    for i in range( s_row, e_row + 1 ):
        for j in range( s_col, e_col + 1 ):
            if board[i][j] != ' ':
                values.append( board[i][j] )

    return list( set(domain).difference( values ) ) # list of values "variable" CAN be.
# check3by3()


# print the sudoku board
def printBoard( board ):
    # print top row
    for col in range(19):
            if col == 0:
                print( '╔', end='' )
            elif col == 18:
                print( '╗' )
            elif col % 6 == 0:
                print( '╦', end='' )
            elif col % 2 == 0:
                print( '╤', end='' )
            else:
                print( '═', end='' )

    # print middle rows
    for row in range(17):
        # print numbers
        if row % 2 == 0:
            for col in range(19):
                if col % 6 == 0:
                    print( '║', end='' )
                elif col % 2 == 0:
                    print( '┆', end='' )
                elif col < 18 and row < 18:
                    print( board[row//2][col//2], end='' )
            print()

        # print row separator
        else:
            for col in range(19):
                if row == 5 or row == 11:
                    if col == 0:
                        print( '╠', end='' )
                    elif col == 18:
                        print( '╣', end='' )
                    elif col % 6 == 0:
                        print( '╬', end='' )
                    elif col % 2 == 0:
                        print( '╪', end='' )
                    else:
                        print( '═', end='' )
                else:
                    if col == 0:
                        print( '╟', end='' )
                    elif col == 18:
                        print( '╢', end='' )
                    elif col % 6 == 0:
                        print( '╫', end='' )
                    elif col % 2 == 0:
                        print( '┼', end='' )
                    else:
                        print( '╌', end='' )
                
            print()

    # print bottom row
    for col in range(19):
        if col == 0:
            print( '╚', end='' )
        elif col == 18:
            print( '╝', end='' )
        elif col % 6 == 0:
            print( '╩', end='' )
        elif col % 2 == 0:
            print( '╧', end='' )
        else:
            print( '═', end='' )

    print()
# printBoard()

# Call Main
main()