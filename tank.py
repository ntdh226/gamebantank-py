# tank.py
import os
import pygame
from constants import TILE_SIZE, TANK_SPEED, COLS, ROWS


class Tank(pygame.sprite.Sprite):
    """Lớp cơ sở cho xe tăng (dùng chung cho Player và Enemy)."""

    def __init__(self, col, row, color, speed=TANK_SPEED, image_path=None):
        super().__init__()

        # Vị trí pixel (chuyển từ tọa độ lưới sang pixel)
        self.x = col * TILE_SIZE
        self.y = row * TILE_SIZE

        self.speed = speed
        self.direction = "UP"  # Hướng mặc định
        self.color = color
        self.size = TILE_SIZE  # Tank chiếm 1 ô = 30px
        self.image_path = image_path

        # Pygame Sprite cần image và rect
        self.base_image = self._load_image(image_path)
        self.image = self.base_image
        if self.image is None:
            self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            self.image.fill(color)
            self.base_image = self.image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self._update_image_for_direction()

    def _load_image(self, image_path):
        if not image_path:
            return None

        full_path = os.path.join(os.path.dirname(__file__), "assets", image_path)
        try:
            image = pygame.image.load(full_path).convert_alpha()
            return pygame.transform.scale(image, (self.size, self.size))
        except (pygame.error, FileNotFoundError):
            return None

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

    def _update_image_for_direction(self):
        """Xoay ảnh theo hướng hiện tại của tank."""
        if self.base_image is None:
            return

        if self.direction == "UP":
            rotated = self.base_image
        elif self.direction == "DOWN":
            rotated = pygame.transform.rotate(self.base_image, 180)
        elif self.direction == "LEFT":
            rotated = pygame.transform.rotate(self.base_image, 90)
        elif self.direction == "RIGHT":
            rotated = pygame.transform.rotate(self.base_image, -90)
        else:
            rotated = self.base_image

        self.image = rotated
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        """Vẽ tank bằng ảnh nếu có, nếu không thì dùng hình vuông màu."""
        self._update_image_for_direction()
        if self.image is not None:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)


class PlayerTank(Tank):
    """Tank do người chơi điều khiển bằng bàn phím."""

    def __init__(self, col=12, row=22):
        super().__init__(
            col,
            row,
            color=(0, 200, 80),
            image_path="Người chơi 1.png",
        )

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

    def __init__(self, col, row, image_path="Xe tăng địch 1.png"):
        super().__init__(
            col,
            row,
            color=(160, 160, 160),
            image_path=image_path,
        )

    def update(self, game_map):
        pass  # TODO: thêm AI di chuyển
