from grid import Grid
from blocks import *
import random

class Game:
    def __init__(self):
        self.k_down_flag = False
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), SBlock(), TBlock(), OBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.hold_block = None
        self.can_hold = True
        self.game_over = False
        self.score = 0

    #updates the score based on the number of lines cleared and the points for moving the block down
    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 200
        elif lines_cleared == 3:
            self.score += 500
        self.score += move_down_points
        print(self.score)

    #returns a random block from the list of available blocks
    def get_random_block(self):
        #If the list of blocks is empty, it re-populates it
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), SBlock(), TBlock(), OBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.k_down_flag = False
        self.blocks.remove(block)
        return block
    
    def hold_current_block(self):
        if not self.can_hold:
            return
        
        # Reset position of current block to top
        self.current_block.reset()
        
        if self.hold_block is None:
            # If no block is held, store current and get new block
            self.hold_block = self.current_block
            self.current_block = self.next_block
            self.next_block = self.get_random_block()
        else:
            # Swap current block with held block
            self.hold_block.reset()  # Reset position of held block
            self.current_block, self.hold_block = self.hold_block, self.current_block
            self.current_block.reset()  # Make sure the new current block starts at top
        
        self.can_hold = False  # Prevent holding again until next block
    
    #This method moves the current block one unit to the left
    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)

    #This method moves the current block one unit to the right
    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)

    #This method moves the current block one unit down
    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()
        self.can_hold = True  # Allow holding again after block moves down

    #This method locks the current block into the grid when it can no longer move down
    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, 0)
        if self.k_down_flag == False:
            self.update_score(0, 1)
        if self.block_fits() == False:
            self.game_over = True

    #Designed to reset the game to its initial state
    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), SBlock(), TBlock(), OBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.hold_block = None
        self.can_hold = True
        self.score = 0

    #Checks whether the current_block can fit into its current position on the grid
    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True

    #Responsible for rotating the current block and checking if the rotated block still fits within the grid
    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()

    #Responsible for checking if the current block is entirely within the grid
    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True
    
    #Responsible for rendering or drawing the game state onto the screen
    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen)