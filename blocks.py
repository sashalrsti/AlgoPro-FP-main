from block import Block
from position import Position
import pygame

class LBlock(Block):
    def __init__(self):
        super().__init__(id = 1)
        self.cells = {
            0: [Position(0, 2), Position (1, 0), Position(1, 1), Position(1,2)],
            1: [Position(0, 1), Position (1, 1), Position(2, 1), Position(2,2)],
            2: [Position(1, 0), Position (1, 1), Position(1, 2), Position(2,0)],
            3: [Position(0, 0), Position (0, 1), Position(1, 1), Position(2,1)]
        }
        self.move(0,3)
        self.texture = pygame.image.load('./assets/sprites/l-block.png').convert_alpha()

class JBlock(Block):
    def __init__(self):
        super().__init__(id = 2)
        self.cells = {
            0: [Position(0, 0), Position (1, 0), Position(1, 1), Position(1,2)],
            1: [Position(0, 1), Position (0, 2), Position(1, 1), Position(2,1)],
            2: [Position(1, 0), Position (1, 1), Position(1, 2), Position(2,2)],
            3: [Position(0, 1), Position (1, 1), Position(2, 0), Position(2,1)]
        }
        self.move(0,3)
        self.texture = pygame.image.load('./assets/sprites/j-block.png').convert_alpha()
        
class IBlock(Block):
    def __init__(self):
        super().__init__(id = 3)
        self.cells = {
            0: [Position(1,0), Position (1, 1), Position(1, 2), Position(1,3)],
            1: [Position(0,2), Position (1, 2), Position(2, 2), Position(3,2)],
            2: [Position(2, 0), Position (2, 1), Position(2, 2), Position(2,3)],
            3: [Position(0, 1), Position (1, 1), Position(2, 1), Position(3,1)]
        }
        self.move(-1,3)
        self.texture = pygame.image.load('./assets/sprites/l-block.png').convert_alpha()

class OBlock(Block):
    def __init__(self):
        super().__init__(id = 4)
        self.cells = {
            0: [Position(0, 0), Position (0,1), Position(1,0), Position(1,1)]
        }
        self.move(0,4)
        self.texture = pygame.image.load('./assets/sprites/o-block.png').convert_alpha()

class SBlock(Block):
    def __init__(self):
        super().__init__(id = 5)
        self.cells = {
            0: [Position(0, 1), Position (0,2), Position(1,0), Position(1,1)],
            1: [Position(0, 1), Position (1,1), Position(1,2), Position(2,2)],
            2: [Position(1, 1), Position (1, 2), Position(2, 0), Position(2,1)],
            3: [Position(0, 0), Position (1,0), Position(1, 1), Position(2,1)]
        }
        self.move(0,3)
        self.texture = pygame.image.load('./assets/sprites/s-block.png').convert_alpha()

class TBlock(Block):
    def __init__(self):
        super().__init__(id = 6)
        self.cells = {
            0: [Position(0, 1), Position (1,0), Position(1,1), Position(1,2)],
            1: [Position(0, 1), Position (1,1), Position(1,2), Position(2,1)],
            2: [Position(1, 0), Position (1, 1), Position(1,2), Position(2,1)],
            3: [Position(0, 1), Position (1,0), Position(1, 1), Position(2,1)]
        }
        self.move(0,3)
        self.texture = pygame.image.load('./assets/sprites/t-block.png').convert_alpha()

class ZBlock(Block):
    def __init__(self):
        super().__init__(id = 7)
        self.cells = {
            0: [Position(0, 0), Position (0,1), Position(1,1), Position(1,2)],
            1: [Position(0, 2), Position (1,1), Position(1,2), Position(2,1)],
            2: [Position(1, 0), Position (1, 1), Position(2,1), Position(2,2)],
            3: [Position(0,1), Position (1,0), Position(1, 1), Position(2,0)]
        }
        self.move(0,3)
        self.texture = pygame.image.load('./assets/sprites/z-block.png').convert_alpha()
