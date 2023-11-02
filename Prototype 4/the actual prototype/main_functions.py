import pygame, os
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
    

def level(screen,player,level):
    enemy, timer_numbers = level_setup(screen,player,level)
    backgrounds = load_level_background(level)
    set_level_positions(screen,player,enemy)
    character_group = add_group([player,enemy])
    healthbar_group = add_group([player.get_health_bar(), enemy.get_health_bar()])
    number_group = add_group(timer_numbers)

    end_level_images = get_endlevel_images()
    pre_level_images = get_prelevel_images(level)

    level_start = False
    level_start_time = pygame.time.get_ticks()
    while not level_start:
        ticks = pygame.time.get_ticks()
        level_start = prelevel_update(screen,ticks,backgrounds,player,enemy,character_group,healthbar_group,number_group,pre_level_images,level_start_time)

    framerate,action_queue,moves,counter_moves,play,defeated,time_left,keydown,level_start_time = level_values()

    if not defeated and time_left:
        defeated,time_left,start_time = main_game(defeated,time_left,screen,framerate,player,enemy,moves,counter_moves,action_queue,keydown,character_group,healthbar_group,number_group,timer_numbers,level_start_time,backgrounds)

    if not time_left and play:
        while play:
            framerate.tick(30)
            ticks = pygame.time.get_ticks()

            play = time_out_update(screen, backgrounds, player, enemy, ticks, character_group, healthbar_group, start_time, end_level_images[2], time_remaining)
            if not play:
                return False

    if defeated and time_left:
        while play:
            framerate.tick(30)
            ticks = pygame.time.get_ticks()
            play = character_defeated_update(screen, backgrounds, player, enemy, ticks, character_group,number_group, healthbar_group, start_time, end_level_images)
                
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



def practice_mode(screen,player):
    dummy = Goku(screen)
    set_level_positions(screen, player, dummy)
    character_group = add_group([player,dummy])
    healthbar_group = add_group([player.get_health_bar(), dummy.get_health_bar()])
    backgrounds = load_level_background(1)
    moves, action_queue, keydown, framerate, previous_list, exit_game, mouse_x, mouse_y = practicemode_game_setup()
    exit_button, button_group = exitbutton_setup(screen)

    while not exit_game:
        framerate.tick(30)
        ticks = pygame.time.get_ticks()

        action_queue, keydown, exit_game, mouse_x, mouse_y = setqueue_eventcheck(action_queue, moves, player, keydown, exit_game,exit_button, mouse_x, mouse_y)
        keypressed = check_true(keydown)

        if not player.get_animating():
            mode, action_queue = character_reaction(player, action_queue)

        dummy_reaction(dummy)
        check_attack_dummy(player, dummy)
        stay_on_screen(player,dummy)

        previous_list = practice_update(screen,backgrounds,player,(mode,keypressed,action_queue,previous_list),dummy,ticks,(healthbar_group,button_group,character_group,),(mouse_x,mouse_y))



def main_game(defeated,time_left,screen,framerate,player,enemy,moves,counter_moves,action_queue,keydown,character_group,healthbar_group,number_group,timer_numbers,level_start_time,backgrounds):
    while not defeated and time_left:
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

        updatescreen_level(screen, backgrounds, player, enemy, ticks, character_group, number_group,healthbar_group, player_mode, enemy_mode, keypressed, time_remaining)


        time_left = check_timer(ticks, level_start_time,player,enemy)
        defeated = check_defeated(player,enemy)
        start_time = get_start_time(ticks, defeated, time_left)

    return defeated,time_left,start_time


def end_level_screen(screen,player,win,current_level):
    level1,level2 = setup_enemy_icons(screen)
    current_enemy = get_current_enemy([level1,level2],current_level)
    next_enemy = get_next_enemy([level1,level2],current_level)
    setup_player_icon(player,win,current_enemy)
    icon_group = add_group([player.get_icon(), level1.get_icon(),level2.get_icon()])
    background = pygame.image.load(os.path.join("spritesheets", "backgrounds", "end_level_background.png"))
    framerate, stop_animating = endlevel_values()

    if next_enemy != None and win or next_enemy == None and not win:
        while not stop_animating:
            framerate.tick(30)
            ticks = pygame.time.get_ticks()

            event_check()

            screen.blit(background,(0,0))
            stop_animating = player.get_icon().update(ticks,180,next_enemy)
            icon_group.draw(screen)
            pygame.display.update()
        

    else:
        print("enemy tree complete")
        

    
    

        
   
        
        
            
    


