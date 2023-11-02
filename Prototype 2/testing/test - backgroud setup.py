import pygame, sys, os
from characterV2 import *
from player_responce2 import *

pygame.init()
screen = pygame.display.set_mode((997,473))

path_background = os.path.join("spritesheets", "Background1", "background.png")
background = pygame.image.load(path_background)

path = os.path.join("spritesheets", "Background1", "background2'.png")
background2 = pygame.image.load(path)

player = Goku(screen)
player._setx(0)
player._sety(player.default_y)
player.default()
group = pygame.sprite.Group()
group.add(player)
framerate = pygame.time.Clock()
moves = set_move()
action_queue = []


while True:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    action_queue = set_queue(action_queue, moves, player)

    if not player.get_animating():
        tuple1 = player_reaction2(player, action_queue)
        mode = tuple1[0]
        action_queue = tuple1[1]

        
            
    screen.blit(background,(0,0))
    screen.blit(background2, (0,269))
    player.update(ticks,180,player._getx(),player._gety(),mode)
    group.draw(screen)
    pygame.display.update()
