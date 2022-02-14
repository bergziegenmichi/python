from random import choice

'''       
--------------------------------------------
           basic functions
'''

def copy_board(board):
    new = {}
    for i in range (1,10):
        new[i] = board[i]
    return new
        
def check_if_game_is_won(board, symbol):
    x = symbol
    b = board
    return ((b[1] == x and b[2] == x and b[3] == x) or
            (b[4] == x and b[5] == x and b[6] == x) or
            (b[7] == x and b[8] == x and b[9] == x) or
            (b[1] == x and b[4] == x and b[7] == x) or
            (b[2] == x and b[5] == x and b[8] == x) or
            (b[3] == x and b[6] == x and b[9] == x) or
            (b[1] == x and b[5] == x and b[9] == x) or
            (b[3] == x and b[5] == x and b[7] == x))

def check_if_game_is_draw(board):
    return(board[1] != '' and board[2] != '' and board[3] != '' and 
           board[4] != '' and board[5] != '' and board[6] != '' and 
           board[7] != '' and board[8] != '' and board[9] != '' )
def random_move(list_with_moves):
    x = choice(list_with_moves)
    return x

def change_board(board, position, symbol):
    new = {}
    for i in range(1,10):
        if i != int(position):
            new[i] = board[i]
        else:
            new[i] = symbol
    return new

def empty_board():
    return {1:'', 2:'', 3:'', 4:'', 5:'', 6:'', 7:'', 8:'', 9:''}

def print_board(board, with_numbers_grid = True):
    left = []
    right = []
    for i in range (1,10):
        y = board[i]
        if y == '':
            y = ' '
        to_append = ' ' + y + ' '
        if i not in [3,6,9]:
            to_append += '|'
        left.append(to_append)
        y = board[i]
        if y == '':
            y = str(i)
        else:
            y = ' '
        to_append = ' ' + y + ' '
        if i not in [3,6,9]:
            to_append += '|'
        right.append(to_append)
    to_print = ''
    if with_numbers_grid == True:
        for i in range(0,7,3):
            for j in range(0,3):
                to_print += left[i+j]
            to_print += 10*' '
            for j in range(0,3):
                to_print += right[i+j]
            if i != 6:
                to_print += '\n---+---+---' + 10*' ' + '---+---+---\n'
    else:
        for i in range(0,7,3):
            for j in range(0,3):
                to_print += left[i+j]
            if i != 6:
                to_print += '\n---+---+---\n'          
    print(to_print)
    
def user_input(board):
    print_board(board)
    user_move = input('Auf welches Feld möchtest du setzen?\n(Schreibe die Zahl) ')
    while True:
        try:
            if board[int(user_move)] == '':
                break
            else:
                user_move = input('Wähle eine gültige Zahl! ')
        except:
            user_move = input('Wähle eine gültige Zahl! ')
    return user_move

def get_symbol():
    symbol = input('Willst du das "X" oder das "O" sein?\nDas Kreuz fängt auch an! ')
    while symbol.lower() not in ['x','o']:
        symbol = input('Erlaubte Eingaben sind "X" und "O"')
    return symbol.upper()

def get_difficulty():
    print('Wählen Sie eine Schwierigkeit!')
    difficulty = input('[E]infach, [S]chwer, [U]nmöglich: ')
    while difficulty.lower() not in ['e','s','u']:
        difficulty = input('Erlaubte Eingaben sind "e", "s", "u".\nGroß- und Kleinschreibung ist egal! ')
    if difficulty.lower() == 'e':
        return 1
    elif difficulty.lower() == 's':
        return 2
    else:
        return 3

def update_score(points_player, points_computer,draws,  winner):
    if winner == 'player':
        points_player += 1
    elif winner == 'computer':
        points_computer += 1
    elif winner == 'draw':
        draws += 1
    return points_player, points_computer, draws

def print_score(points_player, points_computer, draws, rounds_played):
    pp = points_player
    pc = points_computer
    r = rounds_played
    print('Es wurden '+str(r)+' Runden gespielt! Dabei kam es zu folgendem Ergebnis:')
    print('Du hast '+str(pp)+' Punkt(e), ich habe '+str(pc)+' Punkt(e)!')
    print(str(draws)+'-mal war es unentschieden!')
    
def check_total_winner(points_player, points_computer):
    pp = points_player
    pc = points_computer
    if pp == 3:
        return True, 'player'
    elif pc == 3:
        return True, 'computer'
    return False, None

def corner_move(board):
    possible_moves = []
    for i in [1,3,7,9]:
        if board[i] == '':
            possible_moves.append(i)
    return possible_moves

def center_move(board):
    possible_moves = []
    if board[5] == '':
        possible_moves.append(5)
    return possible_moves

def side_move(board):
    possible_moves = []
    for i in [2,4,6,8]:
        if board[i] == '':
            possible_moves.append(i)
    return possible_moves

'''
           basic functions
--------------------------------------------
           simple functions
'''
def test_if_win_is_possible(board, symbol):
    possible_moves = []
    for i in range(1,10):
        board_copy = copy_board(board)
        if board_copy[i] == '':
            board_copy[i] = symbol
            if check_if_game_is_won(board_copy, symbol) == True:
                possible_moves.append(i)
    return possible_moves
'''
           simple functions
--------------------------------------------
           complex functions
'''
def test_if_fork_is_possible(board, symbol):
    possible_fork_moves = []
    for i in range(1,10):
        board_copy = copy_board(board)
        if board_copy[i] == '':
            board_copy[i] = symbol
            possible_win_or_lose_moves = test_if_win_is_possible(board_copy, symbol)
            if len(possible_win_or_lose_moves) > 1:
                possible_fork_moves.append(i)
    return possible_fork_moves


def force_player_to_block(board, symbol):
    if symbol == 'X':
        not_symbol = 'O'
    else:
        not_symbol = 'X'
    possible_forcing_to_block_moves = []
    for i in range(1,10):
        board_copy = copy_board(board)
        if board_copy[i] == '':
            board_copy[i] = symbol
            is_win_possible = test_if_win_is_possible(board_copy, symbol)
            if len(is_win_possible) > 0:
                board_copy[is_win_possible[0]] = not_symbol
                can_player_fork = test_if_win_is_possible(board_copy, not_symbol)
                if len(can_player_fork) < 2:
                    possible_forcing_to_block_moves.append(i)
    return possible_forcing_to_block_moves
'''
           complex functions
--------------------------------------------
'''
force_player_to_block({1: 'X', 2: '', 3: '', 4: '', 5: 'O', 6: '', 7: '', 8: '', 9: 'X'}, 'O' )