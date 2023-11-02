import pygame
from set_up import *
from main_functions import *
from data import *

screen = setup_screen()
player_data = check_data()

while True:
    arcade,practice,controls,exit_select = main_menu(screen)
    if arcade:
        player,player_data = character_select(screen,player_data)
        #win= level(screen,player,1)
        win = True
        end_level_screen(screen,player,win,1)
        if win:
            player_data.set_level_number(1)
            #win = level(screen,player,2)
            win = False
            end_level_screen(screen,player,win,2)
            if win:
                player_data.set_level_number(2)
                player_data.save()
                #^because this is the last level here
            else:
                player_data.save()
        else:
            player_data.save()
            
            
    if practice:
        player = character_select(screen)
        practice_mode(screen,player)
        
    if controls:
        print("added in a a later prototype")
        
    if exit_select:
        exit_game()
