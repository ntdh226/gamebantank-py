# main.py
import pygame
from game import Game

pygame.init()
try:
    pygame.mixer.init()
    AUDIO_ENABLED = True
except pygame.error:
    AUDIO_ENABLED = False
    print("Warning: audio disabled (pygame.mixer.init() failed)")

if __name__ == "__main__":
    game_instance = Game()
    # expose audio availability to game if needed
    game_instance.AUDIO_ENABLED = AUDIO_ENABLED
    game_instance.run()
