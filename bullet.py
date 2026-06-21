# bullet.py
import pygame
from constants import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from obstacle import Obstacle, DESTRUCTIBLE

BULLET_SPEED = 8   # pixels/frame — nhanh hơn tank
BULLET_SIZE  = 6   # px, hình vuông nhỏ


class Bullet(pygame.sprite.Sprite):
    """
    Viên đạn bắn ra từ một tank.

    Thuộc tính:
        owner   : tank đã bắn (để tránh tự bắn mình)
        x, y    : vị trí pixel (tâm đạn)
        dir     : "UP" | "DOWN" | "LEFT" | "RIGHT"
        alive   : False → cần xóa khỏi danh sách
    """

    def __init__(self, tank):
        super().__init__()

        self.owner = tank
        self.dir   = tank.direction
        self.speed = BULLET_SPEED
        self.alive = True

        # Spawn tại tâm nòng súng của tank
        cx = tank.x + tank.size // 2
        cy = tank.y + tank.size // 2

        # Đẩy đạn ra phía trước thêm nửa thân tank
        half = tank.size // 2
        offset = {
            "UP":    (cx,        cy - half),
            "DOWN":  (cx,        cy + half),
            "LEFT":  (cx - half, cy),
            "RIGHT": (cx + half, cy),
        }
        self.x, self.y = offset[self.dir]

        # Pygame sprite
        self.image = pygame.Surface((BULLET_SIZE, BULLET_SIZE))
        self.image.fill((255, 255, 0))  # vàng
        self.rect  = self.image.get_rect(center=(self.x, self.y))

    # ------------------------------------------------------------------
    def update(self, game_map):
        """Di chuyển đạn và kiểm tra va chạm với tường/biên."""
        if not self.alive:
            return

        # Bước 1 — di chuyển
        if self.dir == "UP":
            self.y -= self.speed
        elif self.dir == "DOWN":
            self.y += self.speed
        elif self.dir == "LEFT":
            self.x -= self.speed
        elif self.dir == "RIGHT":
            self.x += self.speed

        self.rect.center = (self.x, self.y)

        # Bước 2 — ra ngoài biên → hủy
        if (self.x < 0 or self.x > SCREEN_WIDTH or
                self.y < 0 or self.y > SCREEN_HEIGHT):
            self.alive = False
            return

        # Bước 3 — kiểm tra ô map tại tâm đạn
        col = int(self.x) // TILE_SIZE
        row = int(self.y) // TILE_SIZE
        tile = game_map.get_tile(col, row)

        if tile == Obstacle.EMPTY or tile == Obstacle.FOREST:
            return  # xuyên qua được

        # Va chạm với tường
        if DESTRUCTIBLE.get(tile, False):
            game_map.set_tile(col, row, Obstacle.EMPTY)  # phá vỡ gạch

        self.alive = False  # đạn nổ

    # ------------------------------------------------------------------
    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(
                screen,
                (255, 220, 0),
                (self.x - BULLET_SIZE // 2,
                 self.y - BULLET_SIZE // 2,
                 BULLET_SIZE, BULLET_SIZE),
            )
