# map.py
import pygame
from obstacle import Obstacle, PASSABLE, COLORS
from constants import ROWS, COLS, TILE_SIZE
from levels.level1 import LEVEL_1
from levels.level2 import LEVEL_2   
class Map:
    def __init__(self):
        self.grid = [[Obstacle.EMPTY] * COLS for _ in range(ROWS)]
        self._load_default("level")
    
    def load_level(self, level_data):
        with open( level_data, "r") as f:
            lines = [line.strip() for line in f.readlines()]

        mapping = {
            ".": Obstacle.EMPTY,
            "B": Obstacle.BRICK,
            "S": Obstacle.STEEL,
            "W": Obstacle.WATER,
            "F": Obstacle.FOREST,
            "x": Obstacle.BASE,
        }
        
        for y, row in enumerate(level_data):
            for x, char in enumerate(row):
                self.grid[y][x] = mapping.get(
                    char,
                    Obstacle.EMPTY,
                )

    def _load_default(self):
        """Map mặc định — đặt BASE ở giữa hàng cuối"""
        base_x = COLS // 2
        base_y = ROWS - 1
        self.grid[base_y][base_x] = Obstacle.BASE

    def get_tile(self, x, y):
        if 0 <= x < COLS and 0 <= y < ROWS:
            return self.grid[y][x]
        return Obstacle.STEEL 

    def is_passable(self, x, y):
        return PASSABLE.get(self.get_tile(x, y), False)

    def set_tile(self, x, y, tile_type):
        if 0 <= x < COLS and 0 <= y < ROWS:
            self.grid[y][x] = tile_type

    def draw(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                tile = self.grid[row][col]
                color = COLORS.get(tile, (0, 0, 0))
                pygame.draw.rect(screen, color,
                    (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))