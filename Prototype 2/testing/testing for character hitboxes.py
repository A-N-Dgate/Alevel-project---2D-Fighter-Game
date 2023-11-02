import pygame
from characterV2 import *
from player_responce2 import *


pygame.init()
screen = pygame.display.set_mode((997,453), 0, 32)

#test character goes here:
player = Raditz(screen)

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
    player.update(ticks,500, player._getx(), player._gety(), mode)
    #500 for animation check; 180 for normal
    
##    pygame.draw.rect(screen, (0,255,0), player.get_rect(), 5)
##    pygame.draw.rect(screen, (255,0,0), player.get_hitbox(), 5)
    #^testing if rect = hitbox
    
    group.draw(screen)

    pygame.display.update()
