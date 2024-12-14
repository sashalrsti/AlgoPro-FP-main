import pygame
import blocks
from colors import Colors

class Grid:
    def __init__(self):
       self.num_rows = 20
       self.num_cols = 10
       self.cell_size = 30
       self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
       self.colors = Colors.get_cell_colors()

    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end = " ")
            print()

    def is_inside(self, row, column):
        if row>= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
            return True
        return False
    
    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False
    
    def is_row_full(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True
    
    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    def move_row_down(self, row, num_rows):
        for column in range(self.num_cols):
            self.grid[row+num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def clear_full_rows(self):
        completed = 0
        for row in range(self.num_rows-1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed
    
    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0
    
    def draw(self, screen):
        # First, draw the grid background if you want (the empty cells)
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column * self.cell_size + 11, row * self.cell_size + 11, self.cell_size - 1, self.cell_size - 1)

                # Draw semi-transparent cell background
                cell_bg = pygame.Surface((self.cell_size - 1, self.cell_size - 1))
                cell_bg.fill(Colors.dark_grey)
                cell_bg.set_alpha(64)  # 25% opacity for cell backgrounds
                screen.blit(cell_bg, cell_rect)
                
                # Draw solid grid lines
                pygame.draw.rect(screen, Colors.light_blue, cell_rect, 1)  # 1 pixel width border

                if cell_value != 0:  # If there's a block here
                    # Get the block corresponding to this cell_value
                    block = self.get_block_by_id(cell_value)
                    if block:
                        # Scale the texture to fit the cell size and draw it
                        scaled_texture = pygame.transform.scale(block.texture, (self.cell_size - 1, self.cell_size - 1))
                        # Convert to alpha and set transparency
                        scaled_texture = scaled_texture.convert_alpha()
                        # Set alpha value (0-255), where 255 is fully opaque
                        scaled_texture.set_alpha(128)  # 50% transparency
                        screen.blit(scaled_texture, cell_rect)
                else:
                    # If it's an empty space, draw a semi-transparent grid cell
                    empty_cell = pygame.Surface((self.cell_size - 1, self.cell_size - 1))
                    empty_cell.fill(Colors.dark_grey)
                    empty_cell.set_alpha(64)  # 25% opacity for empty cells
                    screen.blit(empty_cell, cell_rect)
                    
    def get_block_by_id(self, block_id):
        if block_id == 1:
            return blocks.LBlock()
        elif block_id == 2:
            return blocks.JBlock()
        elif block_id == 3:
            return blocks.IBlock()
        elif block_id == 4:
            return blocks.OBlock()
        elif block_id == 5:
            return blocks.SBlock()
        elif block_id == 6:
            return blocks.TBlock()
        elif block_id == 7:
            return blocks.ZBlock()
        return None
