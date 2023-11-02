import pygame
from set_up import *
from main_functions import *

screen = setup_screen()

while True:
    arcade,practice,controls,exit_select = main_menu(screen)
    if arcade:
        player = character_select(screen)
        win = level(screen,player,1)
        end_level_screen(screen,player,win,1)
        if win:
            win = level(screen,player,2)
            end_level_screen(screen,player,win,2)
            
            
    if practice:
        player = character_select(screen)
        practice_mode(screen,player)
        
    if controls:
        print("added in a a later prototype")
        
    if exit_select:
        exit_game()
