import pygame, time
from set_up import *
from sprite_interactions import *
from update_display import *
from character import *

play = True
defeated = False

screen = setup_screen()
background = load_background("background.png")
framerate = pygame.time.Clock()
player = load_character("Goku", screen)
enemy = load_character("Raditz", screen)
characters = [player, enemy]
group = add_group(characters)
set_positions(player, enemy)


if play:
    while not defeated:
        framerate.tick(30)
        ticks = pygame.time.get_ticks()
        
        if not player.get_animating():
            mode = player_reaction(player)
        enemy_reaction(enemy)
        stay_on_screen(player, enemy)
        check_attack(player, enemy, group)
        if player.get_default_mode():
            player._sety(295)
        update_screen(screen, background, player, enemy, ticks, group, mode)

        defeated = check_defeated(player, enemy)
        start_time = get_start_time(ticks, defeated)

    while defeated:
        ticks = pygame.time.get_ticks()
        play = defeated_update(screen, background, player, enemy, ticks, group, start_time)
        if not play:
            defeated = False

if not play:
    exit_game()

        

   

    
