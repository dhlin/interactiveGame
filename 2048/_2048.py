"""
2048 GUI
"""

import simplegui
import codeskulptor
import math

# Tile Images
IMAGENAME = "assets_2048.png"
TILE_SIZE = 100
HALF_TILE_SIZE = TILE_SIZE / 2
BORDER_SIZE = 45

# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

class GUI:
    """
    Class to run game GUI.
    """

    def __init__(self, game):
        self._game = game
        url = codeskulptor.file2url(IMAGENAME)
        self._tiles = simplegui.load_image(url)
        self._directions = {"up": UP, "down": DOWN,
                            "left": LEFT, "right": RIGHT}
        self._rows = game.get_grid_height()
        self._cols = game.get_grid_width()
        self._frame = simplegui.create_frame('2048',
                        self._cols * TILE_SIZE + 2 * BORDER_SIZE,
                        self._rows * TILE_SIZE + 2 * BORDER_SIZE)
        self._frame.add_button('New Game', self.start)
        self._frame.set_keydown_handler(self.keydown)
        self._frame.set_draw_handler(self.draw)        
        self._frame.set_canvas_background("#A39480")
        self._frame.start()

    def keydown(self, key):
        """
        Keydown handler
        """
        for dirstr, dirval in self._directions.items():
            if key == simplegui.KEY_MAP[dirstr]:
                self._game.move(dirval)
                break

    def draw(self, canvas):
        """
        Draw handler
        """
        for row in range(self._rows):
            for col in range(self._cols):
                tile = self._game.get_tile(row, col)
                if tile == 0:
                    val = 0
                else:
                    val = int(math.log(tile, 2))
                canvas.draw_image(self._tiles,
                    [HALF_TILE_SIZE + val * TILE_SIZE, HALF_TILE_SIZE],
                    [TILE_SIZE, TILE_SIZE],
                    [col * TILE_SIZE + HALF_TILE_SIZE + BORDER_SIZE,
                     row * TILE_SIZE + HALF_TILE_SIZE + BORDER_SIZE],
                    [TILE_SIZE, TILE_SIZE])

    def start(self):
        """
        Start the game.
        """
        self._game.reset()

def run_gui(game):
    """
    Instantiate and run the GUI.
    """
    gui = GUI(game)
    gui.start()
              
import random

# Offsets for computing tile indices in each direction.   
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    temp_list = [0 for dummy_i in range(len(line))]
    temp_list_i = 0
    zero_flag = True
    for dummy_i in range(len(line) - 1):   
        zero_flag = True
        if line[dummy_i] == 0:
            continue
        else:    
            for dummy_i_2 in range(dummy_i + 1, len(line)):
                if line[dummy_i_2] == 0:
                    continue
                elif line[dummy_i] == line[dummy_i_2]:
                    temp_list[temp_list_i] = line[dummy_i] + line[dummy_i_2]
                    line[dummy_i_2] = 0
                    temp_list_i += 1
                    zero_flag = False
                    break
                elif line[dummy_i] != line[dummy_i_2]:
                    temp_list[temp_list_i] = line[dummy_i]
                    temp_list_i += 1
                    zero_flag = False
                    break
            if zero_flag == True:                
                temp_list[temp_list_i] = line[dummy_i]
                break
    if zero_flag == False or line[-1] != 0:
        temp_list[temp_list_i] = line[-1]
    return temp_list

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.row = grid_height
        self.col = grid_width
        self.board = [[0 for dummy_col in range(self.col)] for dummy_row in range(self.row)]
        self.initial_entries = {UP: [(0, i) for i in range(self.col)],
                                DOWN: [(self.row - 1, i) for i in range(self.col)],
                                LEFT: [(i, 0) for i in range(self.row)],
                                RIGHT: [(i, self.col - 1) for i in range(self.row)]}
        
    def reset(self):
        """
        Empty the grid
        """
        self.board = [[0 for dummy_row in range(self.col)] for dummy_col in range(self.row)]
        self.new_tile()
        self.new_tile()
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        s = ""
        for dummy_row in range(self.col):
            for dummy_col in range(self.row):
                s += str(self.board[dummy_row][dummy_col]) + ','
            s = s[:-1] + '\n'
        return s
     

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.row
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.col
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        initial_entries = self.initial_entries[direction]
        offset = OFFSETS[direction]

        if direction == 3 or direction == 4:
            row_or_col = self.col 
        else:
            row_or_col = self.row 
        
        for entry in initial_entries:
            temp_list = merge([self.board[entry[0] + offset[0] * i][entry[1] + offset[1] * i] for i in range(row_or_col)])           
            for count_i in range(row_or_col):
                self.board[entry[0] + offset[0] * count_i][entry[1] + offset[1] * count_i] = temp_list[count_i] 
                                
        self.new_tile()
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty square.  
        The tile should be 2 90% of the time and 4 10% of the time.
        """
        zero_number = 0
        nonzero_flag = False
        for col in range(self.col):
            for row in range(self.row):
                if self.board[row][col] == 0:
                    zero_number += 1
        if zero_number > 0:
            nonzero_flag = True
        while nonzero_flag:                  
            number = random.choice(range(self.row * self.col))
            if self.board[number / (self.col)][number % self.col] == 0:
                self.board[number / (self.col)][number % self.col] = random.choice([2] * 9 + [4] * 1)
                nonzero_flag = False
       
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self.board[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.board[row][col]       

run_gui(TwentyFortyEight(4, 4))
