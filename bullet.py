import pygame
import os
from constants import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from obstacle import Obstacle, DESTRUCTIBLE

BULLET_SPEED = 8
BULLET_SIZE = 16

CURRENT_DIR = os.path.dirname(__file__)
IMAGE_PATH = os.path.join(CURRENT_DIR, "assets", "images", "bullet.png")

try:
    BULLET_IMAGE = pygame.image.load(IMAGE_PATH).convert_alpha()
    BULLET_IMAGE = pygame.transform.scale(BULLET_IMAGE, (BULLET_SIZE, BULLET_SIZE))
except (pygame.error, FileNotFoundError):
    BULLET_IMAGE = pygame.Surface((BULLET_SIZE, BULLET_SIZE))
    BULLET_IMAGE.fill((255, 220, 0))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, tank):
        super().__init__()

        self.owner = tank
        self.dir = tank.direction
        self.speed = BULLET_SPEED
        self.alive = True
        self.hit_base = False  # True neu vien dan nay da ban trung Base
        self.image = BULLET_IMAGE

        cx = tank.x + tank.size // 2
        cy = tank.y + tank.size // 2

        half = tank.size // 2
        spawn_buffer = half + (BULLET_SIZE // 2) + 2

        offset = {
            "UP": (cx, cy - spawn_buffer),
            "DOWN": (cx, cy + spawn_buffer),
            "LEFT": (cx - spawn_buffer, cy),
            "RIGHT": (cx + spawn_buffer, cy),
        }
        self.x, self.y = offset[self.dir]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, game_map):
        if not self.alive:
            return

        if self.dir == "UP":
            self.y -= self.speed
        elif self.dir == "DOWN":
            self.y += self.speed
        elif self.dir == "LEFT":
            self.x -= self.speed
        elif self.dir == "RIGHT":
            self.x += self.speed

        self.rect.center = (self.x, self.y)

        if (
            self.rect.left < 0
            or self.rect.right > SCREEN_WIDTH
            or self.rect.top < 0
            or self.rect.bottom > SCREEN_HEIGHT
        ):
            self.alive = False
            return

        col = int(self.x) // TILE_SIZE
        row = int(self.y) // TILE_SIZE
        tile = game_map.get_tile(col, row)

        if tile == Obstacle.EMPTY or tile == Obstacle.FOREST:
            return

        # YEU CAU: dan trung Base (bat ke ai ban) -> bao cho Game biet de thua
        if tile == Obstacle.BASE:
            self.hit_base = True
            game_map.set_tile(col, row, Obstacle.EMPTY)
            self.alive = False
            return

        if DESTRUCTIBLE.get(tile, False):
            game_map.set_tile(col, row, Obstacle.EMPTY)

        self.alive = False

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.rect)
