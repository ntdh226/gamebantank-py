# tank.py
import pygame
from constants import TILE_SIZE, TANK_SPEED, COLS, ROWS


class Tank(pygame.sprite.Sprite):
    """Lớp cơ sở cho xe tăng (dùng chung cho Player và Enemy)."""

    def __init__(self, col, row, color, speed=TANK_SPEED):
        super().__init__()

        # Vị trí pixel (chuyển từ tọa độ lưới sang pixel)
        self.x = col * TILE_SIZE
        self.y = row * TILE_SIZE

        self.speed = speed
        self.direction = "UP"  # Hướng mặc định
        self.color = color
        self.size = TILE_SIZE  # Tank chiếm 1 ô = 30px

        # Pygame Sprite cần image và rect
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def move(self, direction, game_map):
        """Di chuyển tank nếu không bị chặn bởi tường hoặc biên màn hình."""
        self.direction = direction

        # Tính vị trí mới dựa theo hướng
        new_x = self.x
        new_y = self.y

        if direction == "UP":
            new_y -= self.speed
        elif direction == "DOWN":
            new_y += self.speed
        elif direction == "LEFT":
            new_x -= self.speed
        elif direction == "RIGHT":
            new_x += self.speed

        # Giới hạn trong màn hình
        new_x = max(0, min(new_x, (COLS - 1) * TILE_SIZE))
        new_y = max(0, min(new_y, (ROWS - 1) * TILE_SIZE))

        # Chỉ di chuyển nếu không va chạm tường
        if self._is_passable(new_x, new_y, game_map):
            self.x = new_x
            self.y = new_y
            self.rect.topleft = (self.x, self.y)

    def _is_passable(self, x, y, game_map):
        """
        Kiểm tra 2 góc của cạnh phía trước tank có đi được không.

        Tank size = 30px. Dùng (size - 1) = 29 để lấy pixel cuối cùng
        của tank, tránh tính sang ô kế bên khi chưa thực sự chạm.
        """
        s = self.size - 1  # = 29 (pixel cuối cùng của tank)

        if self.direction == "UP":
            top_left_col = x // TILE_SIZE
            top_right_col = (x + s) // TILE_SIZE
            row = y // TILE_SIZE
            return game_map.is_passable(top_left_col, row) and game_map.is_passable(
                top_right_col, row
            )

        elif self.direction == "DOWN":
            bot_left_col = x // TILE_SIZE
            bot_right_col = (x + s) // TILE_SIZE
            row = (y + s) // TILE_SIZE
            return game_map.is_passable(bot_left_col, row) and game_map.is_passable(
                bot_right_col, row
            )

        elif self.direction == "LEFT":
            col = x // TILE_SIZE
            top_row = y // TILE_SIZE
            bot_row = (y + s) // TILE_SIZE
            return game_map.is_passable(col, top_row) and game_map.is_passable(
                col, bot_row
            )

        elif self.direction == "RIGHT":
            col = (x + s) // TILE_SIZE
            top_row = y // TILE_SIZE
            bot_row = (y + s) // TILE_SIZE
            return game_map.is_passable(col, top_row) and game_map.is_passable(
                col, bot_row
            )

        return True

    def draw(self, screen):
        """Vẽ thân xe và nòng súng."""
        # Vẽ thân xe
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        # Vẽ nòng súng
        self._draw_barrel(screen)

    def _draw_barrel(self, screen):
        """Vẽ nòng súng nhỏ để biết tank đang nhìn hướng nào."""
        cx = self.x + self.size // 2
        cy = self.y + self.size // 2
        barrel_color = (40, 40, 40)

        if self.direction == "UP":
            pygame.draw.rect(screen, barrel_color, (cx - 3, self.y, 6, 12))
        elif self.direction == "DOWN":
            pygame.draw.rect(
                screen, barrel_color, (cx - 3, self.y + self.size - 12, 6, 12)
            )
        elif self.direction == "LEFT":
            pygame.draw.rect(screen, barrel_color, (self.x, cy - 3, 12, 6))
        elif self.direction == "RIGHT":
            pygame.draw.rect(
                screen, barrel_color, (self.x + self.size - 12, cy - 3, 12, 6)
            )


class PlayerTank(Tank):
    """Tank do người chơi điều khiển bằng bàn phím."""

    def __init__(self, col=12, row=22):
        super().__init__(col, row, color=(0, 200, 80))

    def update(self, game_map):
        """Đọc phím bấm và di chuyển — gọi mỗi frame."""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move("UP", game_map)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move("DOWN", game_map)
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move("LEFT", game_map)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move("RIGHT", game_map)


class EnemyTank(Tank):
    """Tank địch — AI sẽ được thêm vào sau."""

    def __init__(self, col, row):
        super().__init__(col, row, color=(160, 160, 160))

    def update(self, game_map):
        pass  # TODO: thêm AI di chuyển
