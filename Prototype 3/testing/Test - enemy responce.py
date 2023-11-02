import pygame, sys
from characterV3 import *
from player_responce import *
from action_classes import *

pygame.init()
screen = pygame.display.set_mode((997,473),0,32)
pygame.display.set_caption("Test - enemy responce")

player = Goku(screen)
enemy = Raditz_enemy(screen)
group = pygame.sprite.Group()
group.add(player)
group.add(enemy)

player._setx(100)
player._sety(player.get_default_y())
enemy._setx(710)
enemy._sety(enemy.get_default_y())
enemy.set_bool_reversed(True)
player.default()
enemy.default()

player_healthbar = health_bar(player,screen,False)
enemy_healthbar = health_bar(enemy,screen,True)
player.set_health_bar(player_healthbar)
enemy.set_health_bar(enemy_healthbar)

framerate = pygame.time.Clock()
moves = set_move()
counter_moves = set_move_enemy()
action_queue = []
keydown = (False, False, False, False)


while True:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

#---------------player reaction-------------------
    
    action_queue, keydown = set_queue(action_queue, moves, player, keydown)
    keypressed = check_true(keydown)

    if not player.get_animating():
        mode, action_queue = player_reaction(player, action_queue)

#---------------enemy reaction-------------------
        
    if not enemy.get_animating():
        enemy.set_queue(counter_moves, player, ticks)
        mode2, queue = player_reaction(enemy, enemy.get_queue())

#--------------------------------------------------
        
    if player.get_attacking():
        enemy.check_attack(player)

    if enemy.get_attacking():
        player.check_attack(enemy)

        
        
    screen.fill((255,255,255))
    player.set_reversed(enemy)
    player.update(ticks, 180, player._getx(), player._gety(), mode, keypressed)
    enemy.set_reversed(player)
    enemy.update(ticks, 180, enemy._getx(), enemy._gety(), mode2, False)
    group.draw(screen)
    player_healthbar.update()
    enemy_healthbar.update()

    pygame.draw.rect(screen, (0,255,0), player.get_hitbox(), 2)
    pygame.draw.rect(screen, (255,0,0), enemy.get_detect_box(), 5)
    pygame.draw.rect(screen, (255,0,0), enemy.get_smaller_detectbox(), 3)
    pygame.draw.rect(screen, (0,0,255), enemy.get_hitbox(), 2)

    pygame.display.update()

    if player.get_health() <= 0:
        player_healthbar.remove_health_rect()
        print("You lost")
        pygame.quit()
        sys.exit()

    if enemy.get_health() <= 0:
        enemy_healthbar.remove_health_rect()
        print("You won")
        pygame.quit()
        sys.exit()
