# enemy.py
import pygame
import random
from constants import TILE_SIZE
from tank import EnemyTank


class Enemy(EnemyTank):
    """Xe tăng địch di chuyển ngẫu nhiên và bắn đạn."""

    def __init__(self, col, row):
        super().__init__(col, row)

        # Đếm frame để đổi hướng
        self.frame_count = 0
        self.change_after = random.randint(30, 60)

        # Đếm frame để bắn đạn
        self.shoot_timer = 0
        self.shoot_delay = random.randint(60, 120)  # Bắn mỗi 1-2 giây

    def update(self, game_map):
        self.frame_count += 1

        # Đổi hướng ngẫu nhiên sau một khoảng thời gian
        if self.frame_count >= self.change_after:
            self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            self.frame_count = 0
            self.change_after = random.randint(30, 60)

        # Di chuyển — dùng move() từ Tank, có check tường sẵn
        self.move(self.direction, game_map)

        # Đếm thời gian bắn
        self.shoot_timer += 1

    def can_shoot(self):
        """Trả về True nếu đến lượt bắn, rồi reset timer."""
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            self.shoot_delay = random.randint(60, 120)
            return True
        return False
