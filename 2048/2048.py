import poc_2048_gui               
import random

# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

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

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
