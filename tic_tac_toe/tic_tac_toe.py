from tic_tac_toe_operations import empty_board, user_input, change_board, check_if_game_is_won,\
check_if_game_is_draw, update_score, print_score, get_difficulty, get_symbol, print_board
from tic_tac_toe_AI import tic_tac_toe_AI as AI

def new_round(player_symbol, difficulty):
    board = empty_board()
    if player_symbol == 'X':
        computer_symbol = 'O'
        computer_moves = [2,4,6,8]
    else:
        computer_symbol = 'X'
        computer_moves = [1,3,5,7,9]
    for i in range(1,10):
        if i in computer_moves:
            move = AI(board, difficulty, player_symbol)
            current_symbol = computer_symbol
        else:
            move = user_input(board)
            current_symbol = player_symbol
        board = change_board(board, move, current_symbol)
            
        game_won = check_if_game_is_won(board, current_symbol)
        if game_won == True:
            print_board(board, False)
            if i in computer_moves:
                return 'computer'
            else:
                return 'player'
        else:
            if check_if_game_is_draw(board) == True:
                print_board(board, False)
                return 'draw'
        
        
        
    
def game(player_symbol, difficulty, points_player, points_computer, draws, rounds_played):
    if player_symbol == 'X':
        computer_symbol = 'O'
    else:
        computer_symbol = 'X'
    winner = new_round(player_symbol, difficulty)
    points_player, points_computer, draws = update_score(points_player, points_computer, draws, winner)
    print_score(points_player, points_computer, draws, rounds_played+1)
    game(computer_symbol, difficulty, points_player, points_computer, draws, rounds_played+1)
    
    
def start():
    player_symbol = get_symbol()
    difficulty = get_difficulty()
    game(player_symbol, difficulty, 0, 0, 0, 0)
    
start()