# enemy.py
import pygame
import random
from constants import TILE_SIZE


class Enemy:
    """Lớp xe tăng địch đơn giản."""

    def __init__(self, col, row):
        """
        Khởi tạo Enemy.
        
        Args:
            col: Cột ban đầu
            row: Hàng ban đầu
        """
        # Vị trí
        self.x = col * TILE_SIZE
        self.y = row * TILE_SIZE
        self.size = TILE_SIZE
        self.speed = 3
        self.color = (160, 160, 160)  # Màu xám
        
        # Hướng di chuyển
        self.direction = "UP"
        
        # Đếm frame để thay đổi hướng
        self.frame_count = 0
        self.change_direction_after = random.randint(30, 60)

    def move(self, game_map):
        """Di chuyển Enemy ngẫu nhiên."""
        # Sau một thời gian, thay đổi hướng
        self.frame_count += 1
        if self.frame_count >= self.change_direction_after:
            self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            self.frame_count = 0
            self.change_direction_after = random.randint(30, 60)
        
        # Tính vị trí mới
        new_x = self.x
        new_y = self.y
        
        if self.direction == "UP":
            new_y -= self.speed
        elif self.direction == "DOWN":
            new_y += self.speed
        elif self.direction == "LEFT":
            new_x -= self.speed
        elif self.direction == "RIGHT":
            new_x += self.speed
        
        # Giới hạn trong màn hình
        max_x = 780 - self.size
        max_y = 780 - self.size
        
        new_x = max(0, min(new_x, max_x))
        new_y = max(0, min(new_y, max_y))
        
        # Cập nhật vị trí
        self.x = new_x
        self.y = new_y

    def draw(self, screen):
        """Vẽ Enemy."""
        # Vẽ hình vuông (tank body)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        
        # Vẽ nòng súng nhỏ để biết hướng
        cx = self.x + self.size // 2
        cy = self.y + self.size // 2
        barrel_color = (100, 100, 100)
        barrel_size = 12
        
        if self.direction == "UP":
            pygame.draw.rect(screen, barrel_color, (cx - 3, self.y, 6, barrel_size))
        elif self.direction == "DOWN":
            pygame.draw.rect(screen, barrel_color, (cx - 3, self.y + self.size - barrel_size, 6, barrel_size))
        elif self.direction == "LEFT":
            pygame.draw.rect(screen, barrel_color, (self.x, cy - 3, barrel_size, 6))
        elif self.direction == "RIGHT":
            pygame.draw.rect(screen, barrel_color, (self.x + self.size - barrel_size, cy - 3, barrel_size, 6))
