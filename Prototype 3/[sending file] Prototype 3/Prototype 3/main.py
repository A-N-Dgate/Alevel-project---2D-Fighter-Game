import pygame
from set_up import *
from main_functions import *

screen = setup_screen()

while True:
    arcade,practice,controls,exit_select = main_menu(screen)
    if arcade:
        player = character_select(screen)
        win = level1(screen,player)
        if win:
            print("player moves on to the next level")
        else:
            print("player has to restart")
    if practice:
        print("added in a a later prototype")
    if controls:
        print("added in a a later prototype")
    if exit_select:
        exit_game()
