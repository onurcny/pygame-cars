import sys
import pygame
import random
from game import Game
from constants import SCREEN_SIZE

pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
game = Game(screen)

while True:
    keys = pygame.key.get_pressed()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("black")
    
    if(game.start):
        game.Update(events)
    else:
        game.GameEnd(events)
        pass

    pygame.display.update()