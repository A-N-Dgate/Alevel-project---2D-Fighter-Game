import pygame, sys
from set_up import *
from character import *

def update_screen(screen, background, player, enemy, ticks, group, mode):
    screen.blit(background, (0,0))
    pygame.draw.rect(screen, (255,0,0), player.get_hitbox(), 5)
    pygame.draw.rect(screen, (0,255,0), enemy.get_hitbox(), 5)
    player.set_reversed(enemy)
    player.update(ticks, 180, player._getx(), player._gety(), mode[0])
    enemy.set_reversed(player)
    enemy.update(ticks, 180, enemy._getx(), enemy._gety(), mode[1])
    group.draw(screen)
    print_text(screen, 0, 0, "player health: %d" %(player.get_health()), 18)
    print_text(screen, 890,0, "enemy health: %d" %(enemy.get_health()), 18)

    
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

def defeated_update(screen, background, player, enemy, ticks, group, start_time):
    screen.blit(background, (0,0))
    pygame.draw.rect(screen, (255,0,0), player.get_hitbox(), 5)
    pygame.draw.rect(screen, (0,255,0), enemy.get_hitbox(), 5)
    
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

def exit_game():
    pygame.quit()
    sys.exit()
    
    
