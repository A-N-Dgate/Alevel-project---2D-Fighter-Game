import pygame, os
from character import *
from player_responce2 import *

pygame.init()
screen = pygame.display.set_mode((997,473), 0, 32)

#character that needs testing here:
player = Vegeta(screen)

enemy = Goku(screen)
group = pygame.sprite.Group()
group.add(player)
group.add(enemy)


player.default()
player._sety(player.get_default_y())
player._setx(0)

enemy.default()
enemy._sety(enemy.get_default_y())
enemy._setx(800)

framerate = pygame.time.Clock()
moves = set_move()
action_queue = []


while True:
    print(player._gety())
    
    framerate.tick(30)
    ticks = pygame.time.get_ticks()
                              
    action_queue = set_queue(action_queue, moves, player)

    if not player.get_animating():
        tuple1 = player_reaction2(player, action_queue)
        mode = tuple1[0]
        action_queue = tuple1[1]


    screen.fill((255,255,255))
    player.set_reversed(enemy)
    enemy.set_reversed(player)
    player.update(ticks, 180, player._getx(), player._gety(), mode, False)
    enemy.update(ticks, 180, enemy._getx(), enemy._gety(), "", False)
    group.draw(screen)

    pygame.display.update()

    
