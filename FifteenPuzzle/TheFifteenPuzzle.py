"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods
    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods
    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods
    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.get_number(target_row, target_col) == 0:
            for solved_num in range(target_row * self._width + target_col + 1, self._width * self._height):
                if self.get_number(solved_num / self._width, solved_num % self._width) != solved_num:
                    return False
            return True 
        else:
            return False        

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        move_string = ""
        current_pos = self.current_position(target_row, target_col)
        assert self.lower_row_invariant(target_row, target_col)
        while(current_pos[0] != self.current_position(0,0)[0]):
            self.update_puzzle('u')
            move_string += 'u'
            
        if current_pos[1] < target_col:           
            while(current_pos[1] != self.current_position(0,0)[1]):
                self.update_puzzle('l')
                move_string += 'l'
            if current_pos[0] == target_row:                
                while(self.get_number(target_row, target_col) != target_row * self._width + target_col):
                    self.update_puzzle("urrdl")
                    move_string += "urrdl"                    
                assert self.lower_row_invariant(target_row, target_col - 1)
                return move_string
            while(self.current_position(target_row, target_col)[1] != target_col):
                self.update_puzzle("drrul")
                move_string += "drrul"
            self.update_puzzle("dru")
            move_string += "dru"
            
        elif current_pos[1] > target_col:          
            while(current_pos[1] != self.current_position(0,0)[1]):
                self.update_puzzle('r')
                move_string += 'r'
            if current_pos[0] == target_row - 1:
                while(self.current_position(target_row, target_col)[1] != target_col):
                    self.update_puzzle("ulldr")
                    move_string += "ulldr"
                self.update_puzzle("ullddruld")
                move_string += "ullddruld" 
                assert self.lower_row_invariant(target_row, target_col - 1)
                return move_string        
            while(self.current_position(target_row, target_col)[1] != target_col):
                self.update_puzzle("dllur")
                move_string += "dllur"
            self.update_puzzle("dlu")
            move_string += "dlu"
                
        while(self.get_number(target_row, target_col) != target_row * self._width + target_col):	
            self.update_puzzle("lddru")
            move_string += "lddru"           
        self.update_puzzle("ld")  
        move_string += "ld"           
                
        assert self.lower_row_invariant(target_row, target_col - 1)
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        move_string = ""
        current_pos = self.current_position(target_row, 0)
        assert self.lower_row_invariant(target_row, 0)
        if current_pos[1] == 0:
            if current_pos[0] == target_row - 1:
                self.update_puzzle('u')
                move_string += 'u'
            else:
                temp_move = target_row - current_pos[0]
                self.update_puzzle('u' * temp_move + "rdl" + "druld" * (temp_move - 2) + "ruldrdlurdluurddlu")
                move_string += ('u' * temp_move + "rdl" + "druld" * (temp_move - 2) + "ruldrdlurdluurddlu")
        elif current_pos[1] > 1:
            temp_move = target_row - current_pos[0]
            self.update_puzzle('u' * temp_move + 'r' * current_pos[1])
            move_string += ('u' * temp_move + 'r' * current_pos[1])  
            temp_move = self.current_position(target_row, 0)[1] - 1
            if current_pos[0] == target_row - 1:               
                self.update_puzzle("ulldr" * temp_move + "ulld")
                move_string += ('u' * temp_move + 'r' * current_pos[1])
            else:
                self.update_puzzle("dllur" * temp_move + "dllu")
                move_string += ("dllur" * temp_move + "dllu")
            temp_move = target_row - self.current_position(target_row, 0)[0]
            self.update_puzzle("druld" * (temp_move - 1) + "ruldrdlurdluurddlu")
            move_string += ("druld" * (temp_move - 1) + "ruldrdlurdluurddlu")
        elif current_pos[1] == 1:
            temp_move = target_row - current_pos[0]
            self.update_puzzle('u' * temp_move + "druld" * (temp_move - 1) + "ruldrdlurdluurddlu")
            move_string += ('u' * temp_move + "druld" * (temp_move - 1) + "ruldrdlurdluurddlu")
        self.update_puzzle('r' * (self._width - 1))
        move_string += ('r' * (self._width - 1))
        assert self.lower_row_invariant(target_row - 1, self._width - 1)   
        return move_string

    #############################################################
    # Phase two methods
    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(0, target_col) == 0:
            for solved_num in range(target_col + 1, self._width * self._height):
                if (solved_num % self._width >= target_col and solved_num / self._width < 2) \
                   and self.get_number(solved_num / self._width, solved_num % self._width) != solved_num:
                    return False
                elif solved_num / self._width >= 2 \
                   and self.get_number(solved_num / self._width, solved_num % self._width) != solved_num:
                    return False
            return True
        else:
            return False           

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(1, target_col) == 0:
            for solved_num in range(0, self._width * self._height):
                if (solved_num % self._width > target_col and solved_num / self._width < 2) \
                   and self.get_number(solved_num / self._width, solved_num % self._width) != solved_num:
                    return False              
                elif (solved_num / self._width >= 2) and \
                    self.get_number(solved_num / self._width, solved_num % self._width) != solved_num:
                    return False
            return True 
        else:
            return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        move_string = ""
        current_pos = self.current_position(0, target_col)
        if current_pos[0] == 0:
            if current_pos[1] == target_col - 1:
                self.update_puzzle('ld')
                move_string += 'ld'
            else:
                temp_move = target_col - current_pos[1] #using calculation to move (abandon loops)
                self.update_puzzle('l' * temp_move + "drrul" * (temp_move - 2) + "dru" + "dlurrdluldrruld")
                move_string += ('l' * temp_move + "drrul" * (temp_move - 2) + "dru" + "dlurrdluldrruld")
        elif current_pos[0] == 1:
            temp_move = target_col - current_pos[1]
            self.update_puzzle('l' * temp_move + "rdlur" * (temp_move - 1) + "dlurrdluldrruld")
            move_string += ('l' * temp_move + "rdlur" * (temp_move - 1) + "dlurrdluldrruld")
        assert self.row1_invariant(target_col - 1)
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        move_string = ""
        current_pos = self.current_position(1, target_col)
        temp_move_col = target_col - current_pos[1] 
        if current_pos[0] == 0:
            if current_pos[1] == target_col:
                self.update_puzzle('u')
                move_string += 'u'
            else:
                self.update_puzzle('u' + 'l' * temp_move_col)
                self.update_puzzle("drrul" * (temp_move_col - 1) + "dru")
                move_string += ('u' + 'l' * temp_move_col + "drrul" * (temp_move_col - 1) + "dru")
        elif current_pos[0] == 1:
            self.update_puzzle('l' * temp_move_col)
            self.update_puzzle("urrdl" * (temp_move_col - 1) + "ur")
            move_string += ('l' * temp_move_col + "urrdl" * (temp_move_col - 1) + "ur")            
        assert self.row0_invariant(target_col)
        return move_string

    ###########################################################
    # Phase 3 methods
    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1)
        if (self.get_number(0,0) == 1 and self.get_number(0,1) == self._width) \
           or (self.get_number(0,0) == self._width and self.get_number(0,1) == self._width + 1) \
           or (self.get_number(0,0) == self._width + 1 and self.get_number(0,1) == 1): 
            return ''
        else:
            move_string = ''
            move_circle = "lurd"
            move_times = 0
            while(self.get_number(0,0) != 0 or self.get_number(0,1) != 1 \
                  or self.get_number(1,0) != self._width or self.get_number(1,1) != self._width + 1):
                self.update_puzzle(move_circle[move_times % 4])
                move_string += move_circle[move_times % 4]
                move_times += 1
            return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ''
        current_zero = self.current_position(0,0)
        self.update_puzzle('r' * (self._width - 1 - current_zero[1]) + 'd' * (self._height - 1 - current_zero[0]))
        move_string += ('r' * (self._width - 1 - current_zero[1]) + 'd' * (self._height - 1 - current_zero[0]))
        for position in range(self._width * self._height - 1, 2 * self._width - 1, -1):
            if (position % self._width) == 0:
                move_string += self.solve_col0_tile(position / self._width)
            else:
                move_string += self.solve_interior_tile(position / self._width, position % self._width)
        for temp_col in range(self._width - 1, 1, -1):
            move_string += self.solve_row1_tile(temp_col)
            move_string += self.solve_row0_tile(temp_col)
        move_string += self.solve_2x2()
        return move_string

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
