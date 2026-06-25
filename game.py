# game.py
import os
import pygame
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    TILE_SIZE,
    STATE_START,
    STATE_PLAYING,
    STATE_GAMEOVER,
)
from map import Map
from tank import PlayerTank
from enemy import Enemy
from bullet import Bullet
from collision import handle_bullet_collisions, check_base_destroyed


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game Ban Tank")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "playing"

        # Font dùng cho UI (start screen / game over screen)
        self.font_title = pygame.font.SysFont(None, 64)
        self.font_text = pygame.font.SysFont(None, 30)

        # State machine: START -> PLAYING -> GAMEOVER -> (PLAYING lại hoặc thoát)
        self.state = STATE_START
        self.playing_level = 1  # Nhớ level đang chơi để "chơi lại đúng màn vừa thua"

        # Các object game thật sự chỉ được tạo khi bấm Start (xem start_level)
        self.map = None
        self.player = None
        self.enemies = []
        self.bullets = []

        self.blink_timer = 0  # Dùng để hiệu ứng nhấp nháy chữ ở màn Start

    # ------------------------------------------------------------------
    def start_level(self, level: int):
        """Khởi tạo (hoặc khởi tạo lại) toàn bộ trạng thái chơi cho 1 level.
        Dùng chung cho cả lúc bắt đầu game lẫn lúc người chơi chọn 'chơi lại'."""
        self.playing_level = level
        self.map = Map(level=level)
        self.player = PlayerTank(col=11, row=22)
        self.enemies = [
            Enemy(col=5, row=2, image_path="Xe tăng địch 1.png"),
            Enemy(col=20, row=2, image_path="Xe tăng địch 2.png"),
            Enemy(col=12, row=2, image_path="Xe tăng địch 3.png"),
        ]
        self.bullets = []
        self.sounds = self._load_sounds()
        self.play_sound("start")

    def _load_sounds(self):
        base_dir = os.path.dirname(__file__)
        sound_paths = {
            "start": os.path.join(base_dir, "assets", "start.mp3"),
            "attack": os.path.join(base_dir, "assets", "attack.mp3"),
            "tank_crack": os.path.join(base_dir, "assets", "tankCrack.mp3"),
        }

        sounds = {}
        for name, path in sound_paths.items():
            try:
                sound = pygame.mixer.Sound(path)
                sound.set_volume(0.35)
                sounds[name] = sound
            except (pygame.error, FileNotFoundError):
                sounds[name] = None
        return sounds

    def play_sound(self, name):
        sound = self.sounds.get(name)
        if sound is not None:
            sound.play()

    # ------------------------------------------------------------------
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    # ------------------------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type != pygame.KEYDOWN:
                continue

            if self.state == STATE_START:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.start_level(1)

            elif self.state == STATE_PLAYING:
                if event.key == pygame.K_SPACE:
                    self.bullets.append(Bullet(self.player))
                    self.play_sound("attack")

            elif self.state == STATE_GAMEOVER:
                if event.key == pygame.K_r:
                    self.start_level(self.playing_level)  # Chơi lại đúng màn vừa thua
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    self.running = False

    # ------------------------------------------------------------------
    def update(self):
        if self.state != STATE_PLAYING:
            return  # Màn Start / Game Over không có logic game để cập nhật

        # 1. Cập nhật player
        self.player.update(self.map)

        # 2. Cập nhật enemy: di chuyển + bắn đạn
        for enemy in self.enemies:
            enemy.update(self.map)
            if enemy.can_shoot():
                self.bullets.append(Bullet(enemy))

        # 3. Cập nhật đạn (di chuyển, check va chạm tường/base bên trong Bullet.update)
        for bullet in self.bullets:
            bullet.update(self.map)

        # 4. YÊU CẦU: đạn (của player hoặc địch) bắn trúng Base -> thua ngay
        #    Phải check TRƯỚC khi lọc bỏ đạn chết, vì đạn trúng base cũng alive=False
        if check_base_destroyed(self.bullets):
            self.state = STATE_GAMEOVER
            return

        # 5. Xóa các viên đạn đã "chết" (bay ra ngoài màn hình / trúng tường / trúng tank)
        self.bullets = [b for b in self.bullets if b.alive]

        # 6. Xử lý va chạm đạn <-> tank (đã lọc theo team trong collision.py)
        all_tanks = [self.player] + self.enemies
        destroyed = handle_bullet_collisions(self.bullets, all_tanks)

        if destroyed:
            self.play_sound("tank_crack")

        # Xóa enemy bị tiêu diệt
        for tank in destroyed:
            if tank in self.enemies:
                self.enemies.remove(tank)

        # 9. Va chạm tank-tank: đẩy player ra nếu đè lên enemy (giữ nguyên logic cũ)
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

        # 10. Hết enemy -> qua level tiếp theo
        if len(self.enemies) == 0:
            self.map.next_level()
            self.playing_level = self.map.current_level
            self.player.x = 11 * TILE_SIZE
            self.player.y = 22 * TILE_SIZE
            self.player.rect.topleft = (self.player.x, self.player.y)
            self.enemies = [
                Enemy(col=5, row=2, image_path="Xe tăng địch 1.png"),
                Enemy(col=20, row=2, image_path="Xe tăng địch 2.png"),
                Enemy(col=12, row=2, image_path="Xe tăng địch 3.png"),
            ]

    # ------------------------------------------------------------------
    def draw(self):
        if self.state == STATE_START:
            self._draw_start_screen()
        elif self.state == STATE_PLAYING:
            self._draw_playing_screen()
        elif self.state == STATE_GAMEOVER:
            self._draw_gameover_screen()

        pygame.display.flip()

    def _draw_start_screen(self):
        self.screen.fill((10, 10, 10))
        title = self.font_title.render("GAME BAN TANK", True, (255, 220, 0))
        self.screen.blit(
            title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        )

        # Nhấp nháy chữ hướng dẫn mỗi 0.5s (30 frame ở FPS=60)
        self.blink_timer += 1
        if (self.blink_timer // 30) % 2 == 0:
            sub = self.font_text.render(
                "Nhan ENTER hoac SPACE de bat dau", True, (255, 255, 255)
            )
            self.screen.blit(
                sub, sub.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
            )

    def _draw_playing_screen(self):
        self.screen.fill((0, 0, 0))
        self.map.draw(self.screen)
        self.player.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw(self.screen)

        text = self.font_text.render(
            f"Level {self.map.current_level}  |  Enemy con: {len(self.enemies)}",
            True,
            (255, 255, 255),
        )
        self.screen.blit(text, (8, 8))

    def _draw_gameover_screen(self):
        self.screen.fill((20, 0, 0))
        title = self.font_title.render("GAME OVER", True, (255, 60, 60))
        self.screen.blit(
            title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        )

        opt1 = self.font_text.render("Nhan R de choi lai", True, (255, 255, 255))
        opt2 = self.font_text.render("Nhan Q de thoat", True, (255, 255, 255))
        self.screen.blit(
            opt1, opt1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        )
        self.screen.blit(
            opt2, opt2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        )
