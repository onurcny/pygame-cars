import pygame
import os

from constants import SCREEN_SIZE, BACKGROUND_PATH

class Background(pygame.sprite.Sprite):
    def __init__(self, y) -> None:
        super().__init__()
        base_path = os.path.dirname(__file__)
        back_path = os.path.join(base_path, "way.png")
        self.image = pygame.image.load(back_path)
        self.rect = pygame.Rect(0, y, SCREEN_SIZE[0], SCREEN_SIZE[1])
    
    def Move(self, speed):
        self.rect.y = self.rect.y+speed
        if self.rect.y >= SCREEN_SIZE[1] * 2:
            self.rect.y = -SCREEN_SIZE[1]

    def getRect(self):
        return self.rect