import pygame
from main_functions import *
from set_up import *
from sprite_interactions import *
from update_display import *

screen = setup_screen()
player = character_select(screen)
level1(screen,player)
exit_game()


