import pygame
from character import *
from update_display import *
from character import *

def player_reaction(player):
    mode = ""
    for event in pygame.event.get():
        if event.type == QUIT:
            exit_game()
            
        user_input = pygame.key.get_pressed()

        #combination keys first - these don't work
        if user_input[K_a] and user_input[K_DOWN]:
            player.low_punch()
            mode = ""

        if user_input[K_x] and user_input[K_DOWN]:
            player.low_kick()
            mode = ""

        if user_input[K_z] and user_input[K_DOWN]:
            player.low_block()
            mode = ""

        if user_input[K_a] and user_input[K_UP]:
            player.uppercut()
            mode = ""

        if user_input[K_x] and user_input[K_UP]:
            player.high_kick()
            mode = ""

        #single keys
        if user_input[K_a]:
            player.punch()
            mode = ""

        if user_input[K_z]:
            player.block()
            mode = ""

        if user_input[K_s]:
            player.chop()
            mode = ""

        if user_input[K_x]:
            player.kick()
            mode = ""

        #directional keys
        if user_input[K_UP]:
            player.jump()
            mode = "jump"
        
        if user_input[K_DOWN]:
            player.crouch()
            mode = ""

        if user_input[K_RIGHT]:
            if player.get_reversed():
                player.move_left()
            else:
                player.move_right()
            mode = "right"

        if user_input[K_LEFT]:
            if player.get_reversed():
                player.move_right()
            else:
                player.move_left()
            mode = "left"

    #if the player isn't doing anything:
    if not player.get_animating():
        if player.get_default_mode():
            #^ to make sure that the first frame isn't reset
            pass
        else:
            player.default()
            mode = ""

#need to test for the number
    if player._gety() <= 234:
        player.back_down()
        mode = "down"

    mode = (mode, "") #"" for the enemy
    return mode


def stay_on_screen(player, enemy):
    #player first:
    if player._gety() < 0:
        player._sety(275)

    if player._getx() > 980 or player._getx() < 0:
        player._setx(0)

    #enemy:
    if enemy._gety() < 0:
        enemy._sety(275)

    if enemy._getx() > 980 or enemy._getx() < 0:
        enemy._setx(0)

def check_attack(player, enemy, group): #not sure if i need the spite group
    #player attack
    if player.get_attacking() and pygame.sprite.collide_rect_ratio(0.9)(player,enemy) and not enemy.get_attacked():
        enemy.set_health(enemy.get_health() - player.get_attack_power())
        enemy.hit()

    #enemy attack
    if enemy.get_attacking() and pygame.sprite.colide_rect_ratio(0.9)(player,enemy) and not player.get_attacked():
        player.set_health(player.get_health() - enemy.get_attack_power())
        player.hit()


def enemy_reaction(enemy):
    if not enemy.get_animating():
        if enemy.get_default_mode():
            pass
        else:
            enemy.default()
    
    
