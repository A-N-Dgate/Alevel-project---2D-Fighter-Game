import pygame
from character import *
from set_up import *
from sprite_interactions import *
from update_display import *


def character_select(screen):
    screen.fill((255,255,255))
    
    path = os.path.join("spritesheets", "backgrounds", "char_select_background.png")
    background = pygame.image.load(path)
    
    lists = character_select_positions(screen)
    character_group = add_group(lists[0])
    select_group = add_group(lists[1])
    framerate = pygame.time.Clock() 

    player_added = False
    x = y = 0

    while not player_added:
        framerate.tick(30)
        ticks = pygame.time.get_ticks()

        x,y, player_selected = select_eventcheck(x,y,lists[1])

        if len(player_selected) != 0:
            op1,op2,op3 = player_selected

            player = character_select_checkclick(op1,op2,op3)
            if player != None:
                player_added = True

        character_select_update(screen,background,character_group,select_group , ticks,lists[0],x,y)

    return player
    

def level1(screen,player):
    screen.fill((255,255,255))
    backgrounds = load_level_background("1") 
    
    enemy = Raditz_enemy(screen)
    characters = [player,enemy]
    group = add_group(characters)
    
    health_bars = set_level_positions(screen,player, enemy)
    healthbar_group = add_group(health_bars)
    player_healthbar = health_bars[0]
    enemy_healthbar = health_bars[1]

    timer_numbers = set_digits()
    number_group = add_group(timer_numbers)

    end_text = get_endlevel_images()
    
    framerate = pygame.time.Clock()
    action_queue = []
    moves = set_move()
    counter_moves = set_move_enemy()

    play = True
    defeated = False
    time_left = True
    keydown = [False,False,False,False]
    level_start_time = set_timer(pygame.time.get_ticks())


    while not defeated and time_left and play:
        framerate.tick(30)
        ticks = pygame.time.get_ticks()

        action_queue, keydown = set_queue(action_queue, moves, player, keydown)
        keypressed = check_true(keydown)

        if not player.get_animating():
            player_mode, action_queue = character_reaction(player,action_queue)

        if not enemy.get_animating():
            enemy.set_queue(counter_moves, player)
            enemy_mode, queue = character_reaction(enemy, enemy.get_queue())

        stay_on_screen(player,enemy)
        check_attacks(player,enemy)

        time_remaining = get_time_remaining(ticks, level_start_time)
        check_number_group(time_remaining, timer_numbers[0], timer_numbers[1], timer_numbers[2])

        updatescreen_level(screen, backgrounds, player, enemy, ticks, group, number_group,healthbar_group, player_mode, enemy_mode, keypressed, time_remaining)

        time_left = check_timer(ticks, level_start_time,player,enemy)
        defeated = check_defeated(player,enemy)
        start_time = get_start_time(ticks, defeated, time_left)

    while not time_left and play:
        framerate.tick(30)
        ticks = pygame.time.get_ticks()

        play = time_out_update(screen, backgrounds, player, enemy, ticks, group, healthbar_group, start_time, end_text[2], time_remaining)
        if not play:
            return False
           
            
    while defeated and time_left and play:
        framerate.tick(30)
        ticks = pygame.time.get_ticks()
        play = character_defeated_update(screen, backgrounds, player, enemy, ticks, group,number_group, healthbar_group, start_time, end_text)
        
        if not play and player.get_dead():
            return False
        elif not play and enemy.get_dead():
            return True


    


        


def main_menu(screen):
    path = os.path.join("spritesheets", "backgrounds", "menu_background.png")
    background = pygame.image.load(path)
    select_sprites = menu_setup(screen)
    select_group = add_group(select_sprites)
    
    framerate = pygame.time.Clock()
    x = y = 0

    while True:
        #^return statement stops the loop
        ticks = pygame.time.get_ticks()
        framerate.tick(30)

        x,y, option_list = select_eventcheck(x,y,select_sprites)

        if len(option_list) != 0:
            op1,op2,op3,op4 = option_list
            boolean_list = menu_checkclick(op1,op2,op3,op4)
            option_selected = check_true(boolean_list)
        else:
            option_selected = False

        if option_selected:
            return boolean_list

        menu_update(screen,select_group, background, x, y)
        
        
        
            
    


