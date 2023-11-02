import pygame, sys
from set_up import *
from character import *


#------------------levels------------------------
def updatescreen_level(screen, background, player, enemy, ticks, group, mode, player_healthbar, enemy_healthbar):
    screen.blit(background[0], (0,0))
    screen.blit(background[1], (0,267))
    pygame.draw.rect(screen, (255,0,0), player.get_hitbox(), 2)
    pygame.draw.rect(screen, (0,255,0), enemy.get_hitbox(), 2)
    player.set_reversed(enemy)
    player.update(ticks, 180, player._getx(), player._gety(), mode)
    enemy.set_reversed(player)
    enemy.update(ticks, 180, enemy._getx(), enemy._gety(), "")
    player_healthbar.update()
    enemy_healthbar.update()
    group.draw(screen)
    
    
    pygame.display.update()

def check_defeated(player, enemy):
    player.set_dead()
    enemy.set_dead()
    
    if player.get_dead():
        player.defeated()
        enemy.default()
        return True
    
    if enemy.get_dead():
        enemy.defeated()
        player.default()
        return True

    else:
        return False

def character_defeated_update(screen, background, player, enemy, ticks, group, start_time):
    screen.blit(background[0], (0,0))
    screen.blit(background[1], (0,267))
    
    if enemy.get_dead():
        print_text(screen, 498.5, 236.5, "YOU WON", 40)
    if player.get_dead():
        print_text(screen, 498.5, 236.5, "PLAYER DEFEATED", 40)
        
    player.set_reversed(enemy)
    player.update(ticks, 180, player._getx(), player._gety(), "")
    enemy.set_reversed(player)
    enemy.update(ticks, 180, enemy._getx(), enemy._gety(), "")
    group.draw(screen)
    pygame.display.update()

    if ticks > start_time + 4000: 
        return False
    else:
        return True

def get_start_time(ticks, defeated):
    if defeated:
        return ticks
    else:
        return 0


#------------------character selection---------------

def character_select_update(screen, character_group,select_group, ticks, characters):
    screen.fill((255,255,255))

    gx, gy =(characters[0].get_select_x(), characters[0].get_default_y()) 
    rx, ry = (characters[1].get_select_x(), characters[1].get_default_y())
    tx, ty = (characters[2].get_select_x(), characters[2].get_default_y())
    
    characters[0].update(ticks, 180,gx,gy, "")
    characters[1].update(ticks, 180,rx,ry, "")
    characters[2].update(ticks, 180, tx, ty, "")
    
    select_group.draw(screen)
    character_group.draw(screen)
    
    pygame.display.update()
    
