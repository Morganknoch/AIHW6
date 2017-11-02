# Authors
#   Luke Mammen
#   Morgan Knoch

import copy
import heapq
import time

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

sudokuBoard2 = [[' ',' ','5',   ' ','1',' ',   ' ',' ',' '],
                [' ',' ','2',   ' ',' ','4',   ' ','3',' '],
                ['1',' ','9',   ' ',' ',' ',   '2',' ','6'],

                ['2',' ',' ',   ' ','3',' ',   ' ',' ',' '],
                [' ','4',' ',   ' ',' ',' ',   '7',' ',' '],
                ['5',' ',' ',   ' ',' ','7',   ' ',' ','1'],

                [' ',' ',' ',   '6',' ','3',   ' ',' ',' '],
                [' ','6',' ',   '1',' ',' ',   ' ',' ',' '],
                [' ',' ',' ',   ' ','7',' ',   ' ','5',' ']]

sudokuBoard3 = [['6','7',' ',   ' ',' ',' ',   ' ',' ',' '],
                [' ','2','5',   ' ',' ',' ',   ' ',' ',' '],
                [' ','9',' ',   '5','6',' ',   '2',' ',' '],

                ['3',' ',' ',   ' ','8',' ',   '9',' ',' '],
                [' ',' ',' ',   ' ',' ',' ',   '8',' ','1'],
                [' ',' ',' ',   '4','7',' ',   ' ',' ',' '],

                [' ',' ','8',   '6',' ',' ',   ' ','9',' '],
                [' ',' ',' ',   ' ',' ',' ',   ' ','1',' '],
                ['1',' ','6',   ' ','5',' ',   ' ','7',' ']]

# the starting domain for each variable
domain = ('1','2','3','4','5','6','7','8','9')

# Contains the blocks and their beginning and ending points
blocks = {1: ((0,0), (2,2)), 2: ((0,3), (2,5)), 3: ((0,6), (2,8)),
          4: ((3,0), (5,2)), 5: ((3,3), (5,5)), 6: ((3,6), (5,8)),
          7: ((6,0), (8,2)), 8: ((6,3), (8,5)), 9: ((6,6), (8,8))}

# Global variables to hold the boards for webpage
board1=None
board2=None
board3=None
board4=None

# Global variable for compute time
computeTime=0

#Global variable to hold variables
countOfVars = 0
firstThreeVars = []

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
        checkConstraints(self, self.board)  # forward checking
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
    global firstThreeVars, countOfVars
    # board 1
    print( "\nBoard 1:")
    board = boardState(sudokuBoard1)
    printBoard(board.board)

    start_time = time.time()
    result = backTrackingSearch( board )
    end_time = time.time() - start_time
    end_time *= 1000                # Convert time in seconds to milliseconds

    if result:
        print( "\nBoard 1 solution:")
        printBoard(board.board)
    else:
        print("\nCould not find solution!\n")

    print("The first chosen variable was " + str(firstThreeVars[0].coords) + " and its domain size was " + str(firstThreeVars[0].mrv) + " and its degree was " + str(firstThreeVars[0].degree))
    print("The second chosen variable was " + str(firstThreeVars[1].coords) + " and its domain size was " + str(firstThreeVars[1].mrv) + " and its degree was " + str(firstThreeVars[1].degree))
    print("The third chosen variable was " + str(firstThreeVars[2].coords) + " and its domain size was " + str(firstThreeVars[2].mrv) + " and its degree was " + str(firstThreeVars[2].degree))
    countOfVars = 0
    firstThreeVars = []

    print("\nCPU execution time: " + str(end_time) + " ms")

    # board 2
    print( "\nBoard 2:")
    board = boardState(sudokuBoard2)
    printBoard(board.board)

    start_time = time.time()
    result = backTrackingSearch( board )
    end_time = time.time() - start_time
    end_time *= 1000                # Convert time in seconds to milliseconds

    if result:
        print( "\nBoard 2 solution:")
        printBoard(board.board)
    else:
        print("\nCould not find solution!")

    print("The first chosen variable was " + str(firstThreeVars[0].coords) + " and its domain size was " + str(firstThreeVars[0].mrv) + " and its degree was " + str(firstThreeVars[0].degree))
    print("The second chosen variable was " + str(firstThreeVars[1].coords) + " and its domain size was " + str(firstThreeVars[1].mrv) + " and its degree was " + str(firstThreeVars[1].degree))
    print("The third chosen variable was " + str(firstThreeVars[2].coords) + " and its domain size was " + str(firstThreeVars[2].mrv) + " and its degree was " + str(firstThreeVars[2].degree))
    countOfVars = 0
    firstThreeVars = []

    print("\nCPU execution time: " + str(end_time) + " ms")

    # board 3
    print( "\nBoard 3:")
    board = boardState(sudokuBoard3)
    printBoard(board.board)

    start_time = time.time()
    result = backTrackingSearch( board )
    end_time = time.time() - start_time
    end_time *= 1000                # Convert time in seconds to milliseconds

    if result:
        print( "\nBoard 3 solution:")
        printBoard(board.board)
    else:
        print("\nCould not find solution!")

    print("The first chosen variable was " + str(firstThreeVars[0].coords) + " and its domain size was " + str(firstThreeVars[0].mrv) + " and its degree was " + str(firstThreeVars[0].degree))
    print("The second chosen variable was " + str(firstThreeVars[1].coords) + " and its domain size was " + str(firstThreeVars[1].mrv) + " and its degree was " + str(firstThreeVars[1].degree))
    print("The third chosen variable was " + str(firstThreeVars[2].coords) + " and its domain size was " + str(firstThreeVars[2].mrv) + " and its degree was " + str(firstThreeVars[2].degree))
    countOfVars = 0
    firstThreeVars = []

    print("\nCPU execution time: " + str(end_time) + " ms")
# main()


# Perform backtracking search on the sudoku puzzle
def backTrackingSearch( boardState ):

    global firstThreeVars, countOfVars    

    if isComplete( boardState ):
        return True

    var = heapq.heappop( boardState.variables )

    if countOfVars < 3:
       hold = copy.deepcopy(var)
       firstThreeVars.append(hold)
       countOfVars += 1

    for value in var.remainingValues:
        makeMove(var, boardState, value)

        if backTrackingSearch( boardState ):
            return True

        heapq.heappush( boardState.variables, var )
        undoMove(var, boardState)

    return False
# backTrackingSearch()


# make move on sudoku puzzle
def makeMove(var, boardState, value):
    boardState.board[var.coords[0]][var.coords[1]] = value
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


# Given a variable and the current board find all of the valid values for it
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
#main()




from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def home():
    global board1, board2, board3, board4, countOfVars, firstThreeVars, computeTime
    if board1:
        hold = render_template('index.html', first=sudokuBoard1, second=sudokuBoard2, third=sudokuBoard3, board1=board1.board, firstThreeVars = firstThreeVars, computeTime=computeTime )
        board1 = None
        countOfVars = 0
        firstThreeVars = []
        computeTime = 0
        return hold
    if board2:
        hold = render_template('index.html', first=sudokuBoard1, second=sudokuBoard2, third=sudokuBoard3, board2=board2.board, firstThreeVars = firstThreeVars, computeTime=computeTime )
        board2 = None
        countOfVars = 0
        firstThreeVars = []
        computeTime = 0
        return hold
    if board3:
        hold = render_template('index.html', first=sudokuBoard1, second=sudokuBoard2, third=sudokuBoard3, board3=board3.board, firstThreeVars = firstThreeVars, computeTime=computeTime )
        board3 = None
        countOfVars = 0
        firstThreeVars = []
        computeTime = 0
        return hold
    if board4:
        hold = render_template('index.html', first=sudokuBoard1, second=sudokuBoard2, third=sudokuBoard3, board4=board4.board, firstThreeVars = firstThreeVars, computeTime=computeTime )
        board4 = None
        countOfVars = 0
        firstThreeVars = []
        computeTime = 0
        return hold

    return render_template('index.html', first=sudokuBoard1, second=sudokuBoard2, third=sudokuBoard3 )

@app.route('/first', methods = ['POST'])
def firstSolution():
    global board1, computeTime
    print( "\nBoard 1:")
    board = boardState(sudokuBoard1)
    printBoard(board.board)

    start_time = time.time()
    result = backTrackingSearch( board )
    end_time = time.time() - start_time
    end_time *= 1000                # Convert time in seconds to milliseconds

    if result:
        print( "\nBoard 1 solution:")
        printBoard(board.board)
    else:
        print("\nCould not find solution!\n")

    print("\nCPU execution time: " + str(end_time) + " ms")

    computeTime = end_time

    board1 = board
    return redirect('/')

@app.route('/second', methods = ['POST'])
def secondSolution():
    global board2, computeTime
    print( "\nBoard 2:")
    board = boardState(sudokuBoard2)
    printBoard(board.board)

    start_time = time.time()
    result = backTrackingSearch( board )
    end_time = time.time() - start_time
    end_time *= 1000                # Convert time in seconds to milliseconds

    if result:
        print( "\nBoard 2 solution:")
        printBoard(board.board)
    else:
        print("\nCould not find solution!\n")

    print("\nCPU execution time: " + str(end_time) + " ms")

    computeTime = end_time

    board2 = board
    return redirect('/')

@app.route('/third', methods = ['POST'])
def thirdSolution():
    global board3, computeTime
    print( "\nBoard 3:")
    board = boardState(sudokuBoard3)
    printBoard(board.board)

    start_time = time.time()
    result = backTrackingSearch( board )
    end_time = time.time() - start_time
    end_time *= 1000                # Convert time in seconds to milliseconds

    if result:
        print( "\nBoard 3 solution:")
        printBoard(board.board)
    else:
        print("\nCould not find solution!\n")

    print("\nCPU execution time: " + str(end_time) + " ms")

    computeTime = end_time
    
    board3 = board
    return redirect('/')

@app.route('/fourth', methods = ['POST'])
def fourthSolution():
    global board4, computeTime
    print( "\nBoard 4:")

    sudokuBoard4 = []
    for a in range(0,9):
        x = []
        for b in range(0,9):
            string = 'input' + str(a) + str(b)
            hold = request.form[string]
            
            if hold.isdigit():
                pass
            else:
                hold = ' '

            x.append(hold)

        sudokuBoard4.append(x)


    board = boardState(sudokuBoard4)  
    printBoard(board.board)

    start_time = time.time()
    result = backTrackingSearch( board )
    end_time = time.time() - start_time
    end_time *= 1000                # Convert time in seconds to milliseconds

    if result:
        print( "\nBoard 4 solution:")
        printBoard(board.board)
    else:
        print("\nCould not find solution!\n")

    print("\nCPU execution time: " + str(end_time) + " ms")

    computeTime = end_time

    board4 = board
    return redirect('/')


if __name__ == '__main__':
    app.run()