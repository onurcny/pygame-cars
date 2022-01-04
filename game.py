from typing import List, Sequence
from pygame.event import Event
from car import Car
from background import Background
from heart import Heart
from constants import CAR_SIZE, SCREEN_SIZE, LOGO_SIZE, TOP_BAR_ICON_SIZE
import pygame
import random
import os


class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.backgrounds = pygame.sprite.Group(
            Background(-SCREEN_SIZE[1]),
            Background(0),
            Background(+SCREEN_SIZE[1])
        )
        self.car_line_index = 1
        self.car = pygame.sprite.GroupSingle(Car((self.car_line_index * 100) + 25, SCREEN_SIZE[1] - CAR_SIZE[1] * 2, False))
        self.cars = pygame.sprite.Group()
        self.heartGroup = pygame.sprite.Group()
        self.speed = 5
        self.enemySpeed = 3
        self.start = False
        self.SpawnCar()
        self.car_spawn_control = 0
        self.hearts = 3
        self.level = 1
        self.max_level = 4
        self.level_control = 0
        self.score = 0
        self.win = False

        self.font_l = pygame.font.SysFont('arial', 26)
        self.font_m = pygame.font.SysFont('arial', 20)
        self.font_s = pygame.font.SysFont('arial', 14)

    def Update(self, events: List[Event]):
        if self.score == 100:
            self.win = True
        if self.win == True:
            self.Win(events)
            return
        self.car_spawn_control = self.car_spawn_control + self.enemySpeed
        if self.car_spawn_control > (CAR_SIZE[1] * 2) + (CAR_SIZE[1] / 2) :
            self.car_spawn_control = 0
            if self.score < 100 - 2:
                for r in range(self.level):
                    self.SpawnCar()
            if self.level < self.max_level:
                self.level_control = self.level_control + 1
            self.score = self.score + 1

        if self.level_control == self.level * 25:
            self.level_control = 0
            self.level= self.level + 1

        for car in self.cars:
            car : Car
            if car.rect.y > SCREEN_SIZE[1]:
                self.cars.remove(car)
            else:
                car.MoveY(self.enemySpeed)
        
        for bg in self.backgrounds:
            bg : Background
            bg.Move(self.speed)

        for h in self.heartGroup:
            h : Heart
            if h.rect.y > SCREEN_SIZE[1]:
                self.heartGroup.remove(h)
            else:
                h.MoveY(self.enemySpeed)

        if self.hearts > 1:
            hits = pygame.sprite.groupcollide(self.car, self.cars, False, True)
            if hits.__len__() > 0:
                self.hearts = self.hearts - 1
        else:
            hits = pygame.sprite.groupcollide(self.car, self.cars, False, False)
            if hits.__len__() > 0:
                self.cars = pygame.sprite.Group()
                self.start = False

        hits = pygame.sprite.groupcollide(self.car, self.heartGroup, False, True)
        self.hearts = self.hearts + hits.__len__()

        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.car_line_index > 0:
                    self.car_line_index = self.car_line_index - 1
                if event.key == pygame.K_RIGHT and self.car_line_index < 2:
                    self.car_line_index = self.car_line_index + 1
                if event.key == pygame.K_ESCAPE:
                    self.start = False
                    return
        self.car.sprite.rect.x = (self.car_line_index * 100) + 25
        self.Draw()

    def Draw(self):
        self.backgrounds.draw(self.screen)
        self.cars.draw(self.screen)
        self.car.draw(self.screen)
        self.DrawTopBar()
        self.heartGroup.draw(self.screen)

    def DrawTopBar(self):
        base_path = os.path.dirname(__file__)
        heart_path = os.path.join(base_path, "heart.png")
        heart = pygame.sprite.Sprite()
        heart.image = pygame.image.load(heart_path)
        heart.image = pygame.transform.scale(heart.image, TOP_BAR_ICON_SIZE)
        heart.rect = heart.image.get_rect()
        heart.rect.x, heart.rect.y = 5, 5
        self.screen.blit(heart.image, heart.rect)

        heart_text = self.font_m.render("x"+str(self.hearts), True, (255, 255, 255))
        heart_text_rect = heart_text.get_rect(center=(15, 15))
        heart_text_rect.x, heart_text_rect.y = 35, 8
        self.screen.blit(heart_text, heart_text_rect)
        
        score_text = self.font_m.render(str(self.score), True, (255, 255, 255))
        score_text_rect = score_text.get_rect(center=(SCREEN_SIZE[0] / 2, 15))
        self.screen.blit(score_text, score_text_rect)

        heart_text = self.font_m.render("x"+str(self.hearts), True, (255, 255, 255))
        rect = heart_text.get_rect(center=(15, 15))
        rect.x, rect.y = 35, 8
        self.screen.blit(heart_text, rect)

    def SpawnCar(self):
        car = Car((random.randint(0, 2) * 100) + 25, -CAR_SIZE[1], True)
        self.cars.add(car)
        if random.randint(0, 100) <= 5:
            self.SpawnHeart(car.rect.x)
    
    def SpawnHeart(self, x):
        self.heartGroup.add(
            Heart(x)
        )

    def Win(self, events: List[Event]):
        for car in self.cars:
            car : Car
            if car.rect.y > SCREEN_SIZE[1]:
                self.cars.remove(car)
            else:
                car.MoveY(self.enemySpeed)
        for bg in self.backgrounds:
            bg : Background
            bg.Move(self.speed)
        self.backgrounds.draw(self.screen)
        self.car.draw(self.screen)

        text = self.font_m.render("Press space key to start...", True, (255, 255, 255))
        rect = text.get_rect(center=(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2))
        self.screen.blit(text, rect)

        text = self.font_l.render("Win!", True, (255, 255, 255))
        rect = text.get_rect(center=(SCREEN_SIZE[0] / 2, 200))
        self.screen.blit(text, rect)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.__init__(self.screen)
                    self.start = True

    def GameEnd(self, events: List[Event]):
        for bg in self.backgrounds:
            bg : Background
            bg.Move(self.speed)
        self.backgrounds.draw(self.screen)
        self.car.draw(self.screen)
        
        base_path = os.path.dirname(__file__)
        logo_path = os.path.join(base_path, "carslogo.png")
        logo = pygame.sprite.Sprite()
        logo.image = pygame.image.load(logo_path)
        logo.image = pygame.transform.scale(logo.image, LOGO_SIZE)
        logo.rect = logo.image.get_rect()
        self.screen.blit(logo.image, logo.rect)

        text = self.font_m.render("Press space key to start...", True, (255, 255, 255))
        rect = text.get_rect(center=(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2))
        self.screen.blit(text, rect)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.__init__(self.screen)
                    self.start = True