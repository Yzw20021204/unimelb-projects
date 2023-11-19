DIR_UP = "u"
DIR_DOWN = "d"
DIR_LEFT = "l"
DIR_RIGHT = "r"
BLANK_PIECE = "Z"

'''Task 1: Pretty Print
Write a function pretty_print(board) that will print the board in a manner that is easy to read. 
You may assume that the board is a correctly formatted list of lists as described on the previous slide. 
Specifically, you should display:

1. On your first line, three spaces, followed by the index values of each column in board, with 0 being the first value. 
Each index value should take up three spaces and be left aligned.
2. On your second line, a row of '-' characters, starting below the first index value printed and ending below the last.
3. Each subsequent line should begin with the index value of a row in board, 
with index value 0 being the first displayed. The index value should take up two spaces and be right aligned. 
The index value should be followed by a '|' character.
4. After the '|' character, each board value in the corresponding row should be printed, 
with two spaces between each value.
5. After the board has been printed, two blank lines should be added.'''

def pretty_print(board):
    '''This function takes a list "board" as input and prints it.
    Forming a board.
    Arg:
        board: A list of lists representing the game board.'''
    
    num_rows = len(board)
    num_colums = len(board[0])
    
    # Print colum index 
    print("   ", end="")
    for colum_index in range(num_colums):
        print(f"{colum_index:<3}", end="")
    print()
    
    # Print the row of '-' characters
    print("   " + "-" * (3 * num_colums))
    
    # Print the number of rows of the board
    for row_index in range(num_rows):
        # Print row index
        print(f"{row_index:>2}|", end="")
        
        # Print row values
        for colum_index in range(num_colums):
            print(f"{board[row_index][colum_index]} ", end=" ")
            
        print()    
        
    # Add blank lines
    print()

'''Task 2: Validate Input
As our game will rely on user-supplied inputs, we wish to ensure those inputs are valid. 
Write a function validate_input(board, position, direction). Your function should ensure:

1. The board contains at least two rows and at least two columns
2. Each row in the board has the same length
3. Each board value is an upper case character
4. The position specified is within the board and does not contain negative row or column values
5. The direction argument contains one of the four permitted direction values
6. For each piece colour present on the board, the number of pieces of that colour is a multiple of four. 
Blanks (represented by 'Z') are not included in this requirement.

Your function should return True if all of the above conditions are satisfied and False otherwise.

Note: You may assume that the board argument contains a list of lists and that each position on the board contains 
a string. You may also assume the position argument is a tuple containing precisely two integer values.'''

def validate_input(board, position, direction):
    '''This function is based on the existing rules of the game to 
    check if the input provided by the user is valid.
    Args:
        board: A list represrnting the game board.
        position: A tuple containing rows and columns of pieces to be moved.
        direction: A string representing the direction the pieces will move.
    Return:
        bool: True if the input is valid, False otherwise.'''

    # 1. The board contains at least two rows and at least tow colums.
    if len(board) < 2 or len(board[0]) < 2:
        return False

    # 2. Each row in the board has the same length.
    row_length = len(board[0])
    for i in board:
        if len(i) != row_length:
            return False

    # 3. Each board value is an upper case characher.
    for row in board:
        for value in row:
            if not value.isupper():
                return False

    # 4. The position specified is within the board and does not cantain
    # negtive row or column values.
    row, column = position
    if row < 0 or column < 0 or row >= len(board) or column >= len(board[0]):
        return False

    # 5. Check if the direction argument cotains one of the four allowed 
    # direction values.
    if direction not in 'u, d, l, r':
        return False

    # 6. For each piece present on the board, the number of pieces of that
    # colour is a multiple of four.
    colour_num = {}
    for row in board:
        for value in row:
            if value != 'Z':
                if value in colour_num:
                    colour_num[value] += 1
                else:
                    colour_num[value] = 1

    for num in colour_num.values():
        if num % 4 != 0:
            return False

    return True

'''Task 3: Legal Move
Recall that a move in our game involves swapping two pieces. A move is legal if:

Both the pieces involved in the move are inside the board
At least one of the pieces involved in the move ends in a position adjacent to a piece of the same colour
Blank pieces (represented with a 'Z') may never be moved.

Write a function legal_move(board, position, direction) that returns True 
if it is legal for the piece at position to be moved in the direction specified by direction and False otherwise.'''

def legal_move(board, position, direction):
    '''This function is based on the existing rules of the game to detect 
    whether the input provided by the user can be legally moved or not.
    Args:
        board: A list representing the game board.
        position: A tuple containing rows and columns of the pieces to be moved
        direction: A string representing the direction the pieces will move.
    Return:
        bool: True if the move is legal, False otherwise.'''

    row, column = position
    row_len = len(board)
    column_len = len(board[0])

    # Defines the direction of movement and its corresponding offset value.
    dic_directions = {
        'u': (-1, 0),
        'd': (1, 0),
        'l': (0, -1),
        'r': (0, 1),
    }

    if direction not in dic_directions:
        return False

    dir_row, dir_column = dic_directions[direction]
    moved_row, moved_column = row + dir_row, column + dir_column

    # (1) The new location should be within the board
    if not (0 <= moved_row < row_len and 0 <= moved_column < column_len):
        return False

    now_piece = board[row][column]
    new_pos = board[moved_row][moved_column]

    # (2) Check if either position contains a blank piece.
    if now_piece == 'Z' or new_pos == 'Z':
        return False

    # Swap the current piece with the piece in the new position. 
    # Simulate movement on the board
    board[row][column], board[moved_row][moved_column] = \
        board[moved_row][moved_column], board[row][column]

    def adj_color(board, row, column):
        '''Check if there are adjacent pieces of the same color'''

        color = board[row][column]
        adj_pos = [(row + dir_row, column + dir_column)
                   for dir_row, dir_column in dic_directions.values()]

        # (3) Find adjacent pieces with the same color.
        for adj_row, adj_col in adj_pos:
            if 0 <= adj_row < row_len and 0 <= adj_col < column_len:
                if board[adj_row][adj_col] == color:
                    return True
        return False

    # Check if there are adjacent pieces of the same color in the original 
    # or new position
    result = adj_color(board, row, column) or \
             adj_color(board, moved_row, moved_column)

    # Pieces end simulation conversion
    board[row][column], board[moved_row][moved_column] = \
        board[moved_row][moved_column], board[row][column]

    return result

'''Task 4: Make Move
If four pieces on the board are moved into position to form a 2 x 2 square, those four pieces are eliminated. 
This leaves a 2 x 2 gap represented by four Z characters which is filled in the following manner:

1. Firstly, all pieces immediately below the gap 
(i.e. in the same column with a higher row index) are moved up to fill any gaps.
2. Secondly, all pieces immediately to the right of the gap 
(i.e. in the same row with a higher column index) are moved left to fill any gaps.
In the event of a tie (i.e. a single move causes more than one 2 x 2 square to be formed), 
the square beginning at the lowest row number is eliminated. If both squares begin at the same row number, 
the square with the lowest column number is eliminated. Only one square may be eliminated before its gaps are filled.'''

def make_move(board, position, direction):
    '''This function takes the board, position, and direction as input to 
    perform the specified move on the board. After this move, 
    it eliminates any adjacent pieces of the same type 
    and moves the remaining pieces up and left to fill the gap.
    Arguments:
        board: A list representing the game board.
        position: A tuple containing rows and columns of the pieces to be moved
        direction: A string representing the direction the pieces will move.
    return:
        List: Modified board after eliminating pieces.'''

    row, column = position
    row_len, column_len = len(board), len(board[0])

    # Defines the direction of movement and its corresponding offset value.
    dic_directions = {
        'u': (-1, 0),
        'd': (1, 0),
        'l': (0, -1),
        'r': (0, 1),
    }

    dir_row, dir_column = dic_directions[direction]
    moved_row, moved_column = row + dir_row, column + dir_column

    # Swap pieces in the original and new positions.
    board[row][column], board[moved_row][moved_column] = \
        board[moved_row][moved_column], board[row][column]

    while True:
        remove = False

        # Check if there are pieces that can be eliminated.
        for r_w in range(row_len - 1):
            for c_n in range(column_len - 1):
                if board[r_w][c_n] == board[r_w][c_n + 1] == \
                        board[r_w + 1][c_n] == board[r_w + 1][c_n + 1] != 'Z':
                    remove = True

                    for i in range(r_w, r_w + 2):
                        for n in range(c_n, c_n + 2):
                            board[i][n] = 'Z'

        if not remove:
            break

        # Move pieces up
        for column in range(column_len):
            empty_row = []
            for row in range(row_len):
                if board[row][column] == 'Z':
                    empty_row.append(row)
                elif empty_row:
                    board[empty_row.pop(0)][column] = board[row][column]
                    board[row][column] = "Z"
                    empty_row.append(row)

        # Move pieces left
        for row in range(row_len):
            empty_column = []
            for column in range(column_len):
                if board[row][column] == 'Z':
                    empty_column.append(column)
                elif empty_column:
                    board[row][empty_column.pop(0)] = board[row][column]
                    board[row][column] = "Z"
                    empty_column.append(column)

    return board     