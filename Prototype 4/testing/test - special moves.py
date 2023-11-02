import pygame, sys
from characterV4 import *
from character_responce import *

pygame.init()
screen = pygame.display.set_mode((997,473))
pygame.display.set_caption("test - special moves")

player = Goku(screen)
group = pygame.sprite.Group()
group.add(player)
player._setx(0)
player._sety(player.get_default_y())
player.default()

framerate = pygame.time.Clock()
moves = set_move()
action_queue = []
keydown = (False, False, False, False) 

#---
#---

while True:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    action_queue, keydown = set_queue(action_queue, moves, player, keydown)
    keypressed = check_true(keydown)

    if not player.get_animating():
        mode, action_queue = character_reaction4(player, action_queue)

    
    screen.fill((255,255,255))
    player.update(ticks, 180, player._getx(), player._gety(), mode, keypressed)
    group.draw(screen)
    
    pygame.display.update()

