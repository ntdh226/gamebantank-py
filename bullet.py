# bullet.py
import pygame
from constants import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from obstacle import Obstacle, DESTRUCTIBLE

BULLET_SPEED = 8
BULLET_SIZE = 16


class Bullet(pygame.sprite.Sprite):
    def __init__(self, tank):
        super().__init__()

        self.owner = tank
        self.dir = tank.direction
        self.speed = BULLET_SPEED
        self.alive = True

        # Spawn tại tâm nòng súng
        cx = tank.x + tank.size // 2
        cy = tank.y + tank.size // 2

        half = tank.size // 2
        offset = {
            "UP": (cx, cy - half),
            "DOWN": (cx, cy + half),
            "LEFT": (cx - half, cy),
            "RIGHT": (cx + half, cy),
        }

        self.x, self.y = offset[self.dir]

        # ===== LOAD ẢNH ĐẠN =====
        self.image = pygame.image.load(
            "assets/images/bullet.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (BULLET_SIZE, BULLET_SIZE)
        )

        self.rect = self.image.get_rect(center=(self.x, self.y))

    # ------------------------------------------------------------------
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
            self.x < 0
            or self.x > SCREEN_WIDTH
            or self.y < 0
            or self.y > SCREEN_HEIGHT
        ):
            self.alive = False
            return

        col = int(self.x) // TILE_SIZE
        row = int(self.y) // TILE_SIZE
        tile = game_map.get_tile(col, row)

        if tile == Obstacle.EMPTY or tile == Obstacle.FOREST:
            return

        if DESTRUCTIBLE.get(tile, False):
            game_map.set_tile(col, row, Obstacle.EMPTY)

        self.alive = False

    # ------------------------------------------------------------------
    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.rect)
