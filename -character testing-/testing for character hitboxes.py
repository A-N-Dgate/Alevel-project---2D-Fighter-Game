import pygame
from character import *
from player_responce2 import *


pygame.init()
screen = pygame.display.set_mode((997,473), 0, 32)

#test character goes here:
player = Goku(screen)

#player.set_bool_reversed(True)

group = pygame.sprite.Group()
group.add(player)

player.default()
player._sety(player.values[0])
player._setx(0)


framerate = pygame.time.Clock()
moves = set_move()
action_queue = []

while True:
    #print(player._gety())

    framerate.tick(30)
    ticks = pygame.time.get_ticks()
        
    action_queue = set_queue(action_queue, moves, player)
    
    if not player.get_animating():
        tuple1 = player_reaction2(player, action_queue)
        mode = tuple1[0]
        action_queue = tuple1[1]

    #so if player animating then queue isnt cleared letting combo keys work


    screen.fill((255,255,255))
    player.update(ticks,500, player._getx(), player._gety(), mode, False)
    #500 for animation check; 180 for normal

    if player.get_attack_box() != None:
        pygame.draw.rect(screen, (0,0,255), player.get_attack_box(), 2)
    
    group.draw(screen)

    pygame.display.update()
