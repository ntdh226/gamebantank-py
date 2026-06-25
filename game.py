# game.py
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TILE_SIZE
from map import Map
from tank import PlayerTank
from enemy import Enemy
from bullet import Bullet
from collision import handle_bullet_collisions


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game Ban Tank")
        self.clock = pygame.time.Clock()
        self.map = Map()
        self.running = True

        self.player = PlayerTank(col=11, row=22)
        self.enemies = [
            Enemy(col=5, row=2),
            Enemy(col=20, row=2),
            Enemy(col=12, row=2),
        ]
        self.bullets = []

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Bắn đạn khi nhấn SPACE
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bullets.append(Bullet(self.player))

    def update(self):
        # Cập nhật player
        self.player.update(self.map)

        # Cập nhật enemy — di chuyển và bắn đạn
        for enemy in self.enemies:
            enemy.update(self.map)
            if enemy.can_shoot():
                self.bullets.append(Bullet(enemy))

        # Cập nhật đạn
        for bullet in self.bullets:
            bullet.update(self.map)

        # Xóa đạn đã chết
        self.bullets = [b for b in self.bullets if b.alive]

        # Xử lý va chạm đạn với tank
        all_tanks = [self.player] + self.enemies
        destroyed = handle_bullet_collisions(self.bullets, all_tanks)

        # Xóa enemy bị tiêu diệt
        for tank in destroyed:
            if tank in self.enemies:
                self.enemies.remove(tank)

        # Va chạm tank-tank: đẩy player ra nếu đè lên enemy
        player_rect = pygame.Rect(
            self.player.x, self.player.y, self.player.size, self.player.size
        )
        for enemy in self.enemies:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.size, enemy.size)
            if player_rect.colliderect(enemy_rect):
                if self.player.direction == "UP":
                    self.player.y += self.player.speed
                elif self.player.direction == "DOWN":
                    self.player.y -= self.player.speed
                elif self.player.direction == "LEFT":
                    self.player.x += self.player.speed
                elif self.player.direction == "RIGHT":
                    self.player.x -= self.player.speed
                self.player.rect.topleft = (self.player.x, self.player.y)

        # Hết enemy thì chuyển level tiếp theo
        if len(self.enemies) == 0:
            self.map.next_level()
            # Reset player về vị trí spawn
            self.player.x = 11 * TILE_SIZE
            self.player.y = 22 * TILE_SIZE
            self.player.rect.topleft = (self.player.x, self.player.y)
            # Spawn lại enemy
            self.enemies = [
                Enemy(col=5, row=2),
                Enemy(col=20, row=2),
                Enemy(col=12, row=2),
            ]

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.map.draw(self.screen)
        self.player.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw(self.screen)

        # HUD — hiện số enemy còn lại và level
        font = pygame.font.SysFont(None, 28)
        text = font.render(
            f"Level {self.map.current_level}  |  Enemy còn: {len(self.enemies)}",
            True,
            (255, 255, 255),
        )
        self.screen.blit(text, (8, 8))

        pygame.display.flip()
