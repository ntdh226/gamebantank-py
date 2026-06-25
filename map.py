# map.py
import pygame
from obstacle import Obstacle, PASSABLE, COLORS
from constants import ROWS, COLS, TILE_SIZE

TOTAL_LEVELS = 3


class Map:
    def __init__(self, level=1):
        self.current_level = level
        self.grid = [[Obstacle.EMPTY] * COLS for _ in range(ROWS)]
        self.load_level(f"levels/level{level}.txt")

        self.images = {
            Obstacle.BRICK: pygame.transform.scale(
                pygame.image.load("assets/brick.png"), (TILE_SIZE, TILE_SIZE)
            ),
            Obstacle.STEEL: pygame.transform.scale(
                pygame.image.load("assets/steel.png"), (TILE_SIZE, TILE_SIZE)
            ),
            Obstacle.WATER: pygame.transform.scale(
                pygame.image.load("assets/water.png"), (TILE_SIZE, TILE_SIZE)
            ),
            Obstacle.FOREST: pygame.transform.scale(
                pygame.image.load("assets/forest.png"), (TILE_SIZE, TILE_SIZE)
            ),
            Obstacle.BASE: pygame.transform.scale(
                pygame.image.load("assets/base.png"), (TILE_SIZE, TILE_SIZE)
            ),
        }

    def load_level(self, filename):
        with open(filename, "r") as f:
            lines = [line.strip() for line in f.readlines()]

        mapping = {
            ".": Obstacle.EMPTY,
            "B": Obstacle.BRICK,
            "S": Obstacle.STEEL,
            "W": Obstacle.WATER,
            "F": Obstacle.FOREST,
            "X": Obstacle.BASE,
        }

        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                self.grid[y][x] = mapping.get(char, Obstacle.EMPTY)

    def next_level(self):
        """Chuyển sang level tiếp theo, xoay vòng 1→2→3→1."""
        next_num = (self.current_level % TOTAL_LEVELS) + 1
        self.current_level = next_num
        self.load_level(f"levels/level{next_num}.txt")

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

                if tile in self.images:
                    screen.blit(self.images[tile], (col * TILE_SIZE, row * TILE_SIZE))
                else:
                    color = COLORS.get(tile, (0, 0, 0))
                    pygame.draw.rect(
                        screen,
                        color,
                        (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    )
