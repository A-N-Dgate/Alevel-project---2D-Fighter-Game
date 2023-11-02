import pygame
from set_up import *
from main_functions import *
from data import *

#bom3 = all characters unlocked
screen = setup_screen()
player_data = check_data()

while True:
    arcade,practice,controls,exit_select = main_menu(screen)
    if arcade:
        player_data = start_arcade(screen, player_data)
        play_char_select_music()
        player = character_select(screen,player_data, True)
        player_data.set_character_name(player.get_name())
        player_data = arcade_mode(screen, player, player_data, 1)
        
    if practice:
        player_data = start_practice(screen, player_data)
        play_char_select_music()
        player = character_select(screen,player_data, True)
        practice_mode(screen,player)
        
    if controls:
        controls_screen(screen)
        
    if exit_select:
        exit_game()
