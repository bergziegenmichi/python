from tic_tac_toe_operations import random_move, test_if_win_is_possible, test_if_fork_is_possible,\
 force_player_to_block, corner_move, center_move, side_move, empty_board

def corner_center_side(board):
    possible_moves = corner_move(board)
    if len(possible_moves) > 0:
        return random_move(possible_moves)

    possible_moves = center_move(board)
    if len(possible_moves) > 0:
        return random_move(possible_moves)

    possible_moves = side_move(board)
    if len(possible_moves) > 0:
        return random_move(possible_moves)
    
def center_corner_side(board):
    possible_moves = center_move(board)
    if len(possible_moves) > 0:
        return random_move(possible_moves)

    possible_moves = corner_move(board)
    if len(possible_moves) > 0:
        return random_move(possible_moves)

    possible_moves = side_move(board)
    if len(possible_moves) > 0:
        return random_move(possible_moves)

def tic_tac_toe_AI(board, difficulty, player_symbol):
    #difficulty:
    #1 = easy
    #2 = difficult
    #3 = impossible
    
    if player_symbol == 'X': 
        computer_symbol = 'O'
    else: 
        computer_symbol = 'X'
    win_moves = test_if_win_is_possible(board, computer_symbol)
    if len(win_moves) > 0:
        return random_move(win_moves)
    lose_moves = test_if_win_is_possible(board, player_symbol)
    if len(lose_moves) > 0:
        return random_move(lose_moves)
    
    if difficulty > 1:
        fork_moves_computer = test_if_fork_is_possible(board, computer_symbol)
        if len(fork_moves_computer) > 0:
            return random_move(fork_moves_computer)
        
        fork_moves_player = test_if_fork_is_possible(board, player_symbol)
        if difficulty == 3 and len(fork_moves_player) > 1:
            possible_moves = force_player_to_block(board, computer_symbol)
            if len(possible_moves) > 0:
                return random_move(possible_moves)
        if len(fork_moves_player) > 0:
            return random_move(fork_moves_player)
        
    if difficulty == 1:
        return corner_center_side(board)
        
    elif difficulty == 2:    
        return center_corner_side(board)
        
    else:
        if board == empty_board():
            return corner_center_side(board)
        else:
            return center_corner_side(board)