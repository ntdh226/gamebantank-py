# game.py
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from map import Map
from tank import PlayerTank


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game Ban Tank")
        self.clock = pygame.time.Clock()
        self.map = Map()
        self.running = True

        # Tạo player — spawn ô (12, 24) gần đáy màn hình
        self.player = PlayerTank(col=12, row=22)

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

    def update(self):
        self.player.update(self.map)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.map.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()
