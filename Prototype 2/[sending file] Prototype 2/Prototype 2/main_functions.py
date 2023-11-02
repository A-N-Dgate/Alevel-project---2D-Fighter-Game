import pygame
from character import *
from set_up import *
from sprite_interactions import *
from update_display import *


def character_select(screen):
    screen.fill((255,255,255))
    pygame.display.set_caption("Select your character")
    lists = character_select_positions(screen)
    character_group = add_group(lists[0])
    select_group = add_group(lists[1])
    framerate = pygame.time.Clock() 
    player_added = False

    while not player_added:
        framerate.tick(30)
        ticks = pygame.time.get_ticks()

        x,y = select_eventcheck()

        player = check_click(lists[1], x,y)
        if player != None:
            player_added = True

        character_select_update(screen,character_group,select_group , ticks,lists[0])

    return player
    

def level1(screen,player):
    screen.fill((255,255,255))
    pygame.display.set_caption("Level 1")
    backgrounds = load_level_background(1) #tuple
    
    enemy = Raditz(screen)
    characters = [player,enemy]
    group = add_group(characters)
    
    health_bars = set_level_positions(screen,player, enemy)
    player_healthbar = health_bars[0]
    enemy_healthbar = health_bars[1]
    
    framerate = pygame.time.Clock()
    action_queue = []
    moves = set_move()
    
    play = True
    defeated = False

    if play:
        while not defeated:
            framerate.tick(30)
            ticks = pygame.time.get_ticks()

            action_queue = set_queue(action_queue, moves, player)

            if not player.get_animating():
                mode_and_queue = player_reaction(player,action_queue)
                action_queue = mode_and_queue[1]

            enemy_reaction(enemy)
            stay_on_screen(player,enemy)
            check_attacks(player,enemy)

            updatescreen_level(screen, backgrounds, player, enemy, ticks, group, mode_and_queue[0], player_healthbar, enemy_healthbar)

            defeated = check_defeated(player,enemy)
            start_time = get_start_time(ticks, defeated)

        while defeated:
            framerate.tick(30)
            ticks = pygame.time.get_ticks()
            play = character_defeated_update(screen, backgrounds, player, enemy, ticks, group, start_time)
            if not play:
                defeated = False              
            
    


