import pygame, sys
from characterV3 import *
from player_responce import *
from action_classes import *

pygame.init()
screen = pygame.display.set_mode((997,473),0,32)
pygame.display.set_caption("Demo - enemy queue")

player = Goku(screen)
enemy = Raditz_enemy(screen)
group = pygame.sprite.Group()
group.add(player)
group.add(enemy)

player._setx(100)
player._sety(player.get_default_y())
enemy._setx(710)
enemy._sety(enemy.get_default_y())
player.default()
enemy.default()

player_healthbar = health_bar(player,screen,False)
enemy_healthbar = health_bar(enemy,screen,True)
player.set_health_bar(player_healthbar)
enemy.set_health_bar(enemy_healthbar)
#^just so error isnt caused when cheking attack collision

framerate = pygame.time.Clock()
moves = set_move()
counter_moves = set_move_enemy()
action_queue = []
keydown = (False, False, False, False)

enemy.test_set_queue([counter_moves[7], counter_moves[7], counter_moves[4], counter_moves[8]])
test = True

while test:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

#---------------player reaction-------------------
    action_queue, keydown = set_queue(action_queue, moves, player, keydown)
    keypressed = check_true(keydown)

    if not player.get_animating():
        mode, action_queue = player_reaction(player, action_queue)

#--------------enemy reaction test----------------

    if not enemy.get_animating():
        mode2, queue = player_reaction(enemy, enemy.get_queue())
        if len(queue) == 0:
            queue = [counter_moves[9]]
        enemy.test_set_queue(queue)


#--------------------------------------------------




        
    screen.fill((255,255,255))
    player.set_reversed(enemy)
    player.update(ticks, 180, player._getx(), player._gety(), mode, keypressed)
    enemy.set_reversed(player)
    enemy.update(ticks, 180, enemy._getx(), enemy._gety(), mode2, False)
    group.draw(screen)

    pygame.draw.rect(screen, (0,255,0), player.get_hitbox(), 2)
    pygame.draw.rect(screen, (0,0,255), enemy.get_hitbox(), 2)

    pygame.display.update()

    if ticks > 5000:
        test = False

pygame.quit()
sys.exit()

