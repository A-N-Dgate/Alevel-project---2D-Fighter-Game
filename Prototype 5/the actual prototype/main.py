import pygame
from set_up import *
from main_functions import *
from data import *

screen = setup_screen()
player_data = check_data()

while True:
    arcade,practice,controls,exit_select = main_menu(screen)
    if arcade:
        player_data = start_arcade(screen, player_data)
        play_char_select_music()
        player = character_select(screen,player_data, True)
        win = level(screen,player,1)
        end_level_screen(screen,player,win,1)
        if win:
            win = level(screen,player,2)
            end_level_screen(screen,player,win,2)
            if win:
                win = level(screen,player,3)
                end_level_screen(screen,player,win,3)
                if win:
                    print("game complete")
                    player_data.set_level_number(3)
                    player_data.save()
                else:
                    player_data.set_level_number(2)
                    player_data.save()
            else:
                player_data.set_level_number(1)
                player_data.save()
        else:
            player_data.save()
            
            
    if practice:
        player_data = start_practice(screen, player_data)
        play_char_select_music()
        player = character_select(screen,player_data, True)
        practice_mode(screen,player)
        
    if controls:
        controls_screen(screen)
        
    if exit_select:
        exit_game()
