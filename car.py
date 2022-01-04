import pygame
import os
from constants import SCREEN_SIZE, CAR_SIZE
import random

from line import Line


class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, isEnemy) -> None:
        super().__init__()
        base_path = os.path.dirname(__file__)
        car_path = os.path.join(base_path, "car.png")
        self.image = pygame.image.load(car_path).convert_alpha()
        if isEnemy:
            self.image.fill("black", special_flags=pygame.BLEND_ADD)
            self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), special_flags=pygame.BLEND_ADD)
        self.rect = pygame.Rect(x, y, CAR_SIZE[0], CAR_SIZE[1])
    
    def MoveY(self, speed):
        self.rect.y = self.rect.y+speed
        # if self.rect.y >= SCREEN_SIZE[1] * 2:
        #     self.rect.y = -SCREEN_SIZE[1]

    def MoveX(self, x):
        self.x = x

    def getRect(self):
        return self.rect