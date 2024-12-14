import pygame
from colors import Colors
from position import Position

class Block():
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 30  # This defines how big each "cell" in the block is
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0
        self.colors = Colors.get_cell_colors()

        # Load the texture (make sure the path is correct)
        self.texture = pygame.image.load('./assets/texture.png').convert_alpha()

    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles
    
    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0
    
    def undo_rotation(self):
        self.rotation_state -= 1
        if self.rotation_state == 0:
            self.rotation_state = len(self.cells) - 1

    def reset(self):
        self.row_offset = 0
        self.column_offset = 3  # Most blocks start at column 3
        self.rotation_state = 0

    def draw(self, screen):
        tiles = self.get_cell_positions()
        for tile in tiles:
            # Create a Rect object to position the texture (scaled to fit cell_size)
            tile_rect = pygame.Rect(tile.column * self.cell_size + 11, tile.row * self.cell_size + 11, self.cell_size - 1, self.cell_size - 1)
            
            # Scale the texture to fit the block size (cell_size) and blit it
            scaled_texture = pygame.transform.scale(self.texture, (self.cell_size - 1, self.cell_size - 1))
            screen.blit(scaled_texture, tile_rect)  # Draw the texture on the screen


