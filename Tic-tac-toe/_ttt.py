# Constants
EMPTY = 1
PLAYERX = 2
PLAYERO = 3 
DRAW = 4

# Map player constants to letters for printing
STRMAP = {EMPTY: " ",
          PLAYERX: "X",
          PLAYERO: "O"}

class TTTBoard:
    """
    Class to represent a Tic-Tac-Toe board.
    """

    def __init__(self, dim, reverse = False, board = None):
        """
        Initialize the TTTBoard object with the given dimension and 
        whether or not the game should be reversed.
        """
 
        self._dim = dim
        self._reverse = reverse
        if board == None:
            # Create empty board
            self._board = [[EMPTY for dummycol in range(dim)] 
                           for dummyrow in range(dim)]
        else:
            # Copy board grid
            self._board = [[board[row][col] for col in range(dim)] 
                           for row in range(dim)]
            
    def __str__(self):
        """
        Human readable representation of the board.
        """
        rep = ""
        for row in range(self._dim):
            for col in range(self._dim):
                rep += STRMAP[self._board[row][col]]
                if col == self._dim - 1:
                    rep += "\n"
                else:
                    rep += " | "
            if row != self._dim - 1:
                rep += "-" * (4 * self._dim - 3)
                rep += "\n"
        return rep

    def get_dim(self):
        """
        Return the dimension of the board.
        """
        return self._dim
    
    def square(self, row, col):
        """
        Returns one of the three constants EMPTY, PLAYERX, or PLAYERO 
        that correspond to the contents of the board at position (row, col).
         """
        return self._board[row][col]

    def get_empty_squares(self):
        """
        Return a list of (row, col) tuples for all empty squares
        """
        empty = []
        for row in range(self._dim):
            for col in range(self._dim):
                if self._board[row][col] == EMPTY:
                    empty.append((row, col))
        return empty

    def move(self, row, col, player):
        """
        Place player on the board at position (row, col).
        player should be either the constant PLAYERX or PLAYERO.
        Does nothing if board square is not empty.
        """
        if self._board[row][col] == EMPTY:
            self._board[row][col] = player

    def check_win(self):
        """
        Returns a constant associated with the state of the game
            If PLAYERX wins, returns PLAYERX.
            If PLAYERO wins, returns PLAYERO.
            If game is drawn, returns DRAW.
            If game is in progress, returns None.
        """
        board = self._board
        dim = self._dim
        dimrng = range(dim)
        lines = []

        # rows
        lines.extend(board)

        # cols
        cols = [[board[rowidx][colidx] for rowidx in dimrng]
                for colidx in dimrng]
        lines.extend(cols)

        # diags
        diag1 = [board[idx][idx] for idx in dimrng]
        diag2 = [board[idx][dim - idx -1] 
                 for idx in dimrng]
        lines.append(diag1)
        lines.append(diag2)

        # check all lines
        for line in lines:
            if len(set(line)) == 1 and line[0] != EMPTY:
                if self._reverse:
                    return switch_player(line[0])
                else:
                    return line[0]

        # no winner, check for draw
        if len(self.get_empty_squares()) == 0:
            return DRAW

        # game is still in progress
        return None
            
    def clone(self):
        """
        Return a copy of the board.
        """
        return TTTBoard(self._dim, self._reverse, self._board)

def switch_player(player):
    """
    Convenience function to switch players.
    
    Returns other player.
    """
    if player == PLAYERX:
        return PLAYERO
    else:
        return PLAYERX

def play_game(mc_move_function, ntrials, reverse = False):
    """
    Function to play a game with two MC players.
    """
    # Setup game
    board = TTTBoard(3, reverse)
    curplayer = PLAYERX
    winner = None
    
    # Run game
    while winner == None:
        # Move
        row, col = mc_move_function(board, curplayer, ntrials)
        board.move(row, col, curplayer)

        # Update state
        winner = board.check_win()
        curplayer = switch_player(curplayer)

        # Display board
        print board
        
    # Print winner
    if winner == PLAYERX:
        print "X wins!"
    elif winner == PLAYERO:
        print "O wins!"
    elif winner == DRAW:
        print "Tie!"
    else:
        print "Error: unknown winner"


"""
Tic Tac Toe GUI code. 
"""

import simplegui

GUI_WIDTH = 400
GUI_HEIGHT = GUI_WIDTH
BAR_WIDTH = 5

class TicTacGUI:
    """
    GUI for Tic Tac Toe game.
    """
    
    def __init__(self, size, aiplayer, aifunction, ntrials, reverse=False):
        # Game board
        self._size = size
        self._bar_spacing = GUI_WIDTH // self._size
        self._turn = PLAYERX
        self._reverse = reverse

        # AI setup
        self._humanplayer = switch_player(aiplayer)
        self._aiplayer = aiplayer
        self._aifunction = aifunction
        self._ntrials = ntrials
        
        # Set up data structures
        self.setup_frame()

        # Start new game
        self.newgame()
        
    def setup_frame(self):
        """
        Create GUI frame and add handlers.
        """
        self._frame = simplegui.create_frame("Tic-Tac-Toe",
                                             GUI_WIDTH,
                                             GUI_HEIGHT)
        self._frame.set_canvas_background('White')
        
        # Set handlers
        self._frame.set_draw_handler(self.draw)
        self._frame.set_mouseclick_handler(self.click)
        self._frame.add_button("New Game", self.newgame)
        self._label = self._frame.add_label("")

    def start(self):
        """
        Start the GUI.
        """
        self._frame.start()

    def newgame(self):
        """
        Start new game.
        """
        self._board = TTTBoard(self._size, self._reverse)
        self._inprogress = True
        self._wait = False
        self._turn = PLAYERX
        self._label.set_text("")
        
    def drawx(self, canvas, pos):
        """
        Draw an X on the given canvas at the given position.
        """
        halfsize = .4 * self._bar_spacing
        canvas.draw_line((pos[0]-halfsize, pos[1]-halfsize),
                         (pos[0]+halfsize, pos[1]+halfsize),
                         BAR_WIDTH, 'Black')
        canvas.draw_line((pos[0]+halfsize, pos[1]-halfsize),
                         (pos[0]-halfsize, pos[1]+halfsize),
                         BAR_WIDTH, 'Black')
        
    def drawo(self, canvas, pos):
        """
        Draw an O on the given canvas at the given position.
        """
        halfsize = .4 * self._bar_spacing
        canvas.draw_circle(pos, halfsize, BAR_WIDTH, 'Black')
        
    def draw(self, canvas):
        """
        Updates the tic-tac-toe GUI.
        """
        # Draw the '#' symbol
        for bar_start in range(self._bar_spacing,
                               GUI_WIDTH - 1,
                               self._bar_spacing):
            canvas.draw_line((bar_start, 0),
                             (bar_start, GUI_HEIGHT),
                             BAR_WIDTH,
                             'Black')
            canvas.draw_line((0, bar_start),
                             (GUI_WIDTH, bar_start),
                             BAR_WIDTH,
                             'Black')
            
        # Draw the current players' moves
        for row in range(self._size):
            for col in range(self._size):
                symbol = self._board.square(row, col)
                coords = self.get_coords_from_grid(row, col)
                if symbol == PLAYERX:
                    self.drawx(canvas, coords)
                elif symbol == PLAYERO:
                    self.drawo(canvas, coords)
                
        # Run AI, if necessary
        if not self._wait:
            self.aimove()
        else:
            self._wait = False
                
    def click(self, position):
        """
        Make human move.
        """
        if self._inprogress and (self._turn == self._humanplayer):        
            row, col = self.get_grid_from_coords(position)
            if self._board.square(row, col) == EMPTY:
                self._board.move(row, col, self._humanplayer)
                self._turn = self._aiplayer
                winner = self._board.check_win()
                if winner is not None:
                    self.game_over(winner)
                self._wait = True
                
    def aimove(self):
        """
        Make AI move.
        """
        if self._inprogress and (self._turn == self._aiplayer):
            row, col = self._aifunction(self._board, 
                                        self._aiplayer, 
                                        self._ntrials)
            if self._board.square(row, col) == EMPTY:
                self._board.move(row, col, self._aiplayer)
            self._turn = self._humanplayer
            winner = self._board.check_win()
            if winner is not None:
                self.game_over(winner)        
            
    def game_over(self, winner):
        """
        Game over
        """
        # Display winner
        if winner == DRAW:
            self._label.set_text("It's a tie!")
        elif winner == PLAYERX:
            self._label.set_text("X Wins!")
        elif winner == PLAYERO:
            self._label.set_text("O Wins!") 
            
        # Game is no longer in progress
        self._inprogress = False

    def get_coords_from_grid(self, row, col):
        """
        Given a grid position in the form (row, col), returns
        the coordinates on the canvas of the center of the grid.
        """
        # X coordinate = (bar spacing) * (col + 1/2)
        # Y coordinate = height - (bar spacing) * (row + 1/2)
        return (self._bar_spacing * (col + 1.0/2.0), # x
                self._bar_spacing * (row + 1.0/2.0)) # y
    
    def get_grid_from_coords(self, position):
        """
        Given coordinates on a canvas, gets the indices of
        the grid.
        """
        posx, posy = position
        return (posy // self._bar_spacing, # row
                posx // self._bar_spacing) # col


def run_gui(board_size, ai_player, ai_function, ntrials, reverse=False):
    """
    Instantiate and run the GUI
    """
    gui = TicTacGUI(board_size, ai_player, ai_function, ntrials, reverse)
    gui.start()


"""
Monte Carlo Tic-Tac-Toe Player
"""

import random

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
            player = switch_player(player)

def mc_update_scores(scores, board, player):
    """
    update the score board
    consider the status of player and winner
    """
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.check_win() == PLAYERX:       
                if player == PLAYERX and board.square(row, col) == PLAYERX:
                    scores[row][col] += MCMATCH 
                elif player == PLAYERX and board.square(row, col) == PLAYERO:
                    scores[row][col] -= MCOTHER
                elif player == PLAYERO and board.square(row, col) == PLAYERX:
                    scores[row][col] += MCOTHER
                elif player == PLAYERO and board.square(row, col) == PLAYERO:
                    scores[row][col] -= MCMATCH                 
                
            elif board.check_win() == PLAYERO:
                if player == PLAYERX and board.square(row, col) == PLAYERX:
                    scores[row][col] -= MCMATCH 
                elif player == PLAYERX and board.square(row, col) == PLAYERO:
                    scores[row][col] += MCOTHER
                elif player == PLAYERO and board.square(row, col) == PLAYERX:
                    scores[row][col] -= MCOTHER
                elif player == PLAYERO and board.square(row, col) == PLAYERO:
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
              
# run the game        
run_gui(3, PLAYERX, mc_move, NTRIALS, False)

