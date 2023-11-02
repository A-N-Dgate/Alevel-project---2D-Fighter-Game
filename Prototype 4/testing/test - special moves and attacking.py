import pygame, sys
from characterV4 import *
from character_responce import *
from level_top_display import *

pygame.init()
screen = pygame.display.set_mode((997,473))
pygame.display.set_caption("test - special moves")

player = Frieza(screen)
group = pygame.sprite.Group()
group.add(player)
player._setx(0)
player._sety(player.get_default_y())
player.default()


enemy = Raditz_enemy(screen)
enemy._setx(400)
enemy._sety(enemy.get_default_y())
enemy.set_bool_reversed(True)
enemy.default()
group.add(enemy)

player.set_health_bar(health_bar(player,screen,False))
enemy.set_health_bar(health_bar(enemy,screen,True))
healthbar_group = pygame.sprite.Group()
healthbar_group.add(player.get_health_bar())
healthbar_group.add(enemy.get_health_bar())

framerate = pygame.time.Clock()
moves = set_move()
counter_moves = set_move_enemy()
action_queue = []
keydown = (False, False, False, False)

while True:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    action_queue, keydown = set_queue(action_queue, moves, player, keydown)
    keypressed = check_true(keydown)

    if not player.get_animating():
        mode, action_queue = character_reaction4(player, action_queue)

##    if not enemy.get_animating(): 
##        enemy.set_queue(counter_moves, player)
##        mode2, queue = character_reaction(enemy, enemy.get_queue())

    if player.get_attacking():
        enemy.check_attack(player)

##    if enemy.get_attacking():
##        player.check_attack(enemy)

    if not enemy.get_animating():
        if enemy.get_default_mode():
            pass
        else:
            enemy.default()
        
    screen.fill((255,255,255))
    player.set_reversed(enemy)
    player.update(ticks, 180, player._getx(), player._gety(), mode, keypressed)
    enemy.set_reversed(player)
    enemy.update(ticks, 180, enemy._getx(), enemy._gety(), "", False)
    healthbar_group.update()
    healthbar_group.draw(screen)
    group.draw(screen)

    pygame.draw.rect(screen, (255,0,0), enemy.get_hitbox(), 2)
    
    pygame.display.update()

    if enemy.get_health() <= 0:
        print("player wins")
        pygame.quit()
        sys.exit()

    if player.get_health() <= 0:
        print("enemy wins")
        pygame.quit()
        sys.exit()

