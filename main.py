# main.py
import pygame
from game import Game

pygame.init()
pygame.mixer.init()

if __name__ == '__main__':
    game_instance = Game()
    game_instance.run()