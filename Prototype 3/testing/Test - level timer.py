import pygame, sys
from characterV3 import *
from player_responce import *
from action_classes import *
from number_class import *


        

pygame.init()
screen = pygame.display.set_mode((997,473),0,32)
pygame.display.set_caption("Test - level timer")

player = Goku(screen)
enemy = Raditz_enemy(screen)
group = pygame.sprite.Group()
group.add(player)
group.add(enemy)

#--for displaying the time remaining--
digit_1 = number(0)
digit_2 = number(1)
digit_3 = number(2)

number_group = pygame.sprite.Group()

number_group.add(digit_1)
number_group.add(digit_2)
number_group.add(digit_3)
#-------------------------------------

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
health_bar_group = pygame.sprite.Group()
health_bar_group.add(player_healthbar)
health_bar_group.add(enemy_healthbar)

framerate = pygame.time.Clock()
moves = set_move()
counter_moves = set_move_enemy()
action_queue = []
keydown = (False, False, False, False)

level_start_time = set_timer(pygame.time.get_ticks())
play = True

while play:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()
    
    action_queue, keydown = set_queue(action_queue, moves, player, keydown)
    keypressed = check_true(keydown)

    if not player.get_animating():
        mode, action_queue = player_reaction(player, action_queue)
        
    if not enemy.get_animating():
        enemy.set_queue(counter_moves, player, ticks)
        mode2, queue = player_reaction(enemy, enemy.get_queue())
        
    if player.get_attacking():
        enemy.check_attack(player)

    if enemy.get_attacking():
        player.check_attack(enemy)

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

    screen.fill((255,255,255))
    player.set_reversed(enemy)
    player.update(ticks, 180, player._getx(), player._gety(), mode, keypressed)
    enemy.set_reversed(player)
    enemy.update(ticks, 180, enemy._getx(), enemy._gety(), mode2, False)
    group.draw(screen)
    health_bar_group.update()
    health_bar_group.draw(screen)
    
    time_remaining = get_time_remaining(ticks)
    check_number_group(time_remaining, digit_1, digit_2, digit_3)
    number_group.update(time_remaining)
    number_group.draw(screen)

    pygame.display.update()

    #---------checking the time----------------
    play = check_timer(ticks, level_start_time)
    

#if the time has ran out:
if not play: #in Prototype: if not play AND not defeated:
    print("Game Over - Out of Time")
    pygame.quit()
    sys.exit()

