"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 100  # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player

def mc_trial(board, player):
    """
    randomly play the game
    """
    while board.check_win() == None:
        rand_square = random.randrange(len(board.get_empty_squares()))
        board.move(board.get_empty_squares()[rand_square][0], board.get_empty_squares()[rand_square][1], player)
        if board.get_empty_squares() != []:
            player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
    update the score board
    consider the status of player and winner
    """
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.check_win() == provided.PLAYERX:       
                if player == provided.PLAYERX and board.square(row, col) == provided.PLAYERX:
                    scores[row][col] += MCMATCH 
                elif player == provided.PLAYERX and board.square(row, col) == provided.PLAYERO:
                    scores[row][col] -= MCOTHER
                elif player == provided.PLAYERO and board.square(row, col) == provided.PLAYERX:
                    scores[row][col] += MCOTHER
                elif player == provided.PLAYERO and board.square(row, col) == provided.PLAYERO:
                    scores[row][col] -= MCMATCH                 
                
            elif board.check_win() == provided.PLAYERO:
                if player == provided.PLAYERX and board.square(row, col) == provided.PLAYERX:
                    scores[row][col] -= MCMATCH 
                elif player == provided.PLAYERX and board.square(row, col) == provided.PLAYERO:
                    scores[row][col] += MCOTHER
                elif player == provided.PLAYERO and board.square(row, col) == provided.PLAYERX:
                    scores[row][col] -= MCOTHER
                elif player == provided.PLAYERO and board.square(row, col) == provided.PLAYERO:
                    scores[row][col] += MCMATCH

def get_best_move(board, scores):
    """
    find the highest score in scores board and record the location in board
    """
    empty_squares = board.get_empty_squares()
    highest_score = float('-inf')
    highest_score_list = []

    for square in empty_squares:
        if scores[square[0]][square[1]] == highest_score:
            highest_score_list.append(square)
        elif scores[square[0]][square[1]] > highest_score:
            highest_score = scores[square[0]][square[1]]
            highest_score_list = [square]
    #print highest_score_list
    return random.choice(highest_score_list)
            
def mc_move(board, player, trials): 
    """
    get best move
    """
    scores = [ [0.0 for dummy_row in range(board.get_dim())] for dummy_col in range(board.get_dim())]      
    for dummy_times in range(trials):
        clone_board = board.clone()
        mc_trial(clone_board, player)
        mc_update_scores(scores, clone_board, player)
    return get_best_move(board, scores)
              
# auto play
# provided.play_game(mc_move, NTRIALS, False)

# run the game        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

