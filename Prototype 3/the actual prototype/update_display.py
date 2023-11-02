import pygame, sys
from set_up import *
from character import *


#------------------levels------------------------
def updatescreen_level(screen, background, player, enemy, ticks, group,number_group, healthbar_group, player_mode,enemy_mode, keydown, time_remaining):
    screen.blit(background[0], (0,0))
    screen.blit(background[1], (0,267))
    player.set_reversed(enemy)
    player.update(ticks, 180, player._getx(), player._gety(), player_mode,keydown)
    enemy.set_reversed(player)
    enemy.update(ticks, 180, enemy._getx(), enemy._gety(), enemy_mode, False)
    healthbar_group.update()
    healthbar_group.draw(screen)
    number_group.update(time_remaining)
    number_group.draw(screen)
    group.draw(screen)
    
    
    pygame.display.update()

def check_defeated(player, enemy):
    player.set_dead()
    enemy.set_dead()
    
    if player.get_dead():
        player.defeated()
        enemy.default()
        player.get_health_bar().remove_health_rect()
        return True
    
    if enemy.get_dead():
        enemy.defeated()
        player.default()
        enemy.get_health_bar().remove_health_rect()
        return True

    else:
        return False

def character_defeated_update(screen, background, player, enemy, ticks, group,number_group, healthbar_group, start_time, end_text):
    screen.blit(background[0], (0,0))
    screen.blit(background[1], (0,267))
    
    if enemy.get_dead():
        screen.blit(end_text[1],(410,220))
    if player.get_dead():
        screen.blit(end_text[0],(410,220))
        
    player.set_reversed(enemy)
    player.update(ticks, 180, player._getx(), player._gety(), "", False)
    enemy.set_reversed(player)
    enemy.update(ticks, 180, enemy._getx(), enemy._gety(), "", False)
    group.draw(screen)
    healthbar_group.update()
    healthbar_group.draw(screen)
    number_group.draw(screen)
    pygame.display.update()

    if ticks > start_time + 4000: 
        return False
    else:
        return True

def time_out_update(screen, background, player, enemy, ticks, group, healthbar_group, start_time, text, time_remaining):
    screen.blit(background[0], (0,0))
    screen.blit(background[1], (0,267))
    screen.blit(text, (410,220))

    player.set_reversed(enemy)
    player.update(ticks, 180, player._getx(), player._gety(), "", False)
    enemy.set_reversed(player)
    enemy.update(ticks, 180, enemy._getx(), enemy._gety(), "", False)
    group.draw(screen)
    healthbar_group.update()
    healthbar_group.draw(screen)
    pygame.display.update()

    if ticks > start_time + 4000: 
        return False
    else:
        return True

    

def get_start_time(ticks, defeated, time_left):
    if defeated or not time_left:
        return ticks
    else:
        return 0

def check_timer(current_time, level_start_time, player, enemy):
    if (current_time - level_start_time) // 1000 <= 300: 
        return True
    else:
        player.defeated()
        enemy.default()
        return False


def get_time_remaining(current_time, level_start_time):
    time_remaining = 300 - ((current_time- level_start_time) // 1000)
    if time_remaining < 0:
        time_remaining = 0
    return time_remaining

def check_number_group(time_remaining, digit_1, digit_2, digit_3):
    if time_remaining < 100 and digit_1.alive():
        digit_1.kill()
        digit_2.set_digit(0)
        digit_3.set_digit(1)
        digit_2.set_x_value((digit_2.get_x_value() + 7))
        digit_3.set_x_value((digit_3.get_x_value() + 7))
    elif time_remaining < 10 and digit_2.alive():
        digit_2.kill()
        digit_3.set_digit(0)
        digit_3.set_x_value((digit_3.get_x_value() + 7))


#------------------character selection---------------

def character_select_update(screen,background, character_group,select_group, ticks, characters,x, y):

    gx, gy =(characters[0].get_select_x(), characters[0].get_default_y()) 
    rx, ry = (characters[1].get_select_x(), characters[1].get_default_y())
    tx, ty = (characters[2].get_select_x(), characters[2].get_default_y())
    
    characters[0].update(ticks, 180,gx,gy, "", False)
    characters[1].update(ticks, 180,rx,ry, "", False)
    characters[2].update(ticks, 180, tx, ty, "", False)

    screen.blit(background, (0,0))
    select_group.update(x,y)
    select_group.draw(screen)
    character_group.draw(screen)
    
    pygame.display.update()

#------------------main_menu----------------------

def menu_update(screen, select_group, background, mouse_x, mouse_y):
    screen.blit(background, (0,0))
    select_group.update(mouse_x, mouse_y)
    select_group.draw(screen)

    pygame.display.update()
    

    
