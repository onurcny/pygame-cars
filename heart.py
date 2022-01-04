import pygame
import os
from constants import HEART_SIZE, CAR_SIZE

class Heart(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        base_path = os.path.dirname(__file__)
        back_path = os.path.join(base_path, "heart.png")
        self.image = pygame.image.load(back_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, HEART_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, -(HEART_SIZE[1] + CAR_SIZE[1] + 10)
    
    def MoveY(self, speed):
        self.rect.y = self.rect.y+speed

    def getRect(self):
        return self.rect