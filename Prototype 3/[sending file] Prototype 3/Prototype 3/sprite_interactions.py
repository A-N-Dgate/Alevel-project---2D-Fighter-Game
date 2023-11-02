import pygame, sys
from character import *
from update_display import *
from character import *
from action_classes import *
from level_top_display import *

#------------------all---------------------------

def exit_game():
    pygame.quit()
    sys.exit()

def check_true(boolean_list):
    for boolean in boolean_list:
        if boolean == True:
            return True
    return False

#------------------levels------------------------
def stay_on_screen(player, enemy):
    if player._getx() > 980 or player._getx() < 0:
        player._setx(0)

    if enemy._getx() > 980 or enemy._getx() < 0:
        enemy._setx(0)


def enemy_reaction(enemy):
    if not enemy.get_animating():
        if enemy.get_default_mode():
            pass
        else:
            enemy.default()

def level_event_check():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit_game()




def set_queue(action_queue, moves, player, keydown):  
#punch, block, chop, kick, jump, crouch, right, left, down, default

    action_queue.reverse()
    action_taken = moves[9]

    for event in pygame.event.get():
        user_input = pygame.key.get_pressed()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        #single keys
        elif user_input[K_a]:
            action_taken = moves[0]

        elif user_input[K_z]:
            action_taken = moves[1]

        elif user_input[K_s]:
            action_taken = moves[2]

        elif user_input[K_x]:
            action_taken = moves[3]

        #directional keys
        elif user_input[K_UP]:
            action_taken = moves[4]
            
        elif user_input[K_DOWN]:
            action_taken = moves[5]

        elif user_input[K_RIGHT]:
            action_taken = moves[6]

        elif user_input[K_LEFT]:
            action_taken = moves[7]

        else:
            action_taken = moves[9]

        keydown = keydown_check(user_input, keydown)

    if player._gety() <= player.get_highest_y(): 
        action_taken = moves[8]


    try:
        if action_queue[0].get_name() != action_taken.get_name():
            action_queue.append(action_taken)
    except: #queue too small to check
        action_queue.append(action_taken)
            
    action_queue.reverse()
    return action_queue, keydown

def keydown_check(user_input, keydown):
    k1, k2, k3, k4 = keydown
    if user_input[K_z]:
        ke1 = True
    else:
        k1 = False

    if user_input[K_DOWN]:
        k2 = True
    else:
        k2 = False

    if user_input[K_RIGHT]:
        k3 = True
    else:
        k3 = False

    if user_input[K_LEFT]:
        k4 = True
    else:
        k4 = False

    return k1, k2, k3, k4



    

def check_queue(action_queue):
    if len(action_queue) > 1:
        current_move = action_queue[0]

        #so that the program skips default:
        next_in = 1
        try:
            while action_queue[next_in].get_name() == "default": 
                next_in += 1
        except: #list is too small
            return current_move, None
        check_move = action_queue[next_in]


    elif len(action_queue) == 1:
        current_move = action_queue[0]
        check_move = None

    else: #nothing in the queue
        return "", action_queue

    return current_move, check_move

def combination_move_check(current_move, check_move, character, action_queue):
    if not current_move.get_movement() and check_move.get_movement() or current_move.get_movement() and not check_move.get_movement():
        #check each combination
        if check_move.get_name() == "jump":
            if current_move.get_name() == "punch":
               character.uppercut()

            if current_move.get_name() == "kick":
                character.high_kick()

        if current_move.get_name() == "jump":
            if check_move.get_name() == "punch":
                character.uppercut()

            if check_move.get_name() == "kick":
                character.high_kick()

        if check_move.get_name() == "crouch":
            if current_move.get_name() == "punch":
                character.low_punch()

            if current_move.get_name() == "kick":
                character.low_kick()

            if current_move.get_name() == "block":
                player.low_block()

        if current_move.get_name() == "crouch":
            if check_move.get_name() == "punch":
                character.low_punch()

            if check_move.get_name() == "kick":
                character.low_kick()

            if check_move.get_name() == "block":
                character.low_block()
            
        mode = ""
        action_queue = []
        #^since the character will perform an extra move after the combination move

        return action_queue, mode

def single_move_check(current_move,check_move, character, action_queue):
    move_taken = False
    if not current_move.get_movement():
        if current_move.get_name() == "punch":
            character.punch()
            move_taken = True
                
        if current_move.get_name() == "kick":
            character.kick()
            move_taken = True

        if current_move.get_name() == "chop":
            character.chop()
            move_taken = True

        if current_move.get_name() == "block":
            character.block()
            move_taken = True

    if current_move.get_movement():
        if current_move.get_name() == "right":
            if character.get_reversed():
                character.move_left()
            else:
                character.move_right()
            move_taken = True

        if current_move.get_name() == "left":
            if character.get_reversed():
                character.move_right()    
            else:
                character.move_left()
            move_taken = True

        if current_move.get_name() == "jump":
            character.jump()
            move_taken = True

        if current_move.get_name() == "crouch":
            character.crouch()
            move_taken = True

        if current_move.get_name() == "down":
            character.back_down()
            move_taken = True

    if check_move != None and not move_taken:
        if not check_move.get_movement():
            if check_move.get_name() == "punch":
                character.punch()
                    
            if check_move.get_name() == "kick":
                character.kick()

            if check_move.get_name() == "chop":
                character.chop()

            if check_move.get_name() == "block":
                character.block()

        if check_move.get_movement():
            if check_move.get_name() == "right":
                if character.get_reversed():
                    character.move_left()
                else:
                    character.move_right()

            if check_move.get_name() == "left":
                if character.get_reversed():
                    character.move_right()    
                else:
                    character.move_left()

            if check_move.get_name() == "jump":
                character.jump()

            if check_move.get_name() == "crouch":
                character.crouch()

            if check_move.get_name() == "down":
                character.back_down()

        

    mode = current_move.get_mode()
    if len(action_queue) > 0:
        action_queue.remove(action_queue[0])
    return action_queue, mode


def default_check(character, action_queue):
    if not character.get_animating(): 
        if character.get_default_mode():
            #^ to make sure that the first frame isn't reset
            pass
        else:
            character.default()
            if character.get_in_air():
                pass
            else:
                character._sety(character.get_default_y())
                #^so that he y vlaue isnt set to defualt while the player is falling

        if len(action_queue) > 0:
            action_queue.remove(action_queue[0])

    return action_queue

def character_reaction(character, action_queue):
    mode = ""
    current_move, check_move = check_queue(action_queue)
    actionqueue_mode = None

    if current_move == "":
        return "", action_queue

    if check_move != None:
        actionqueue_mode = combination_move_check(current_move, check_move, character, action_queue)

    if actionqueue_mode != None:
        action_queue, mode = actionqueue_mode
    else:
        action_queue, mode = single_move_check(current_move,check_move, character, action_queue)

    action_queue = default_check(character, action_queue)

    if len(action_queue) > 4:
        action_queue = []
        #^failsafe: to stop the queue from being stuck on one move, freezing the game


    return mode, action_queue



def check_attacks(player, enemy):
    if player.get_attacking():
        enemy.check_attack(player)

    if enemy.get_attacking():
        player.check_attack(enemy)



#------------------character selection---------------
    
def select_eventcheck(x,y,sprites):
    item_list = []
    
    for event in pygame.event.get():
        if event.type == QUIT:
            exit_game()

        if event.type == MOUSEMOTION:
            x,y = pygame.mouse.get_pos()

        if event.type == MOUSEBUTTONUP:
            for sprite in sprites:
                item = sprite.check_click(x,y)
                item_list.append(item)
                


    return x,y, item_list


def character_select_checkclick(option1,option2,option3):
    player = None

    if option1 != None or option2 != None or option3 != None:
        if option1 != None:
            player = option1
        if option2 != None:
            player = option2
        if option3 != None:
            player = option3

    return  player

#------------------main menu---------------------

def menu_checkclick(option1,option2,option3,option4):
# return booleans(arcade,practice,controls,exit)
    if option1 or option2 or option3 or option4:
        if option1:
            return (True,False,False,False)
        if option2:
            return (False,True,False,False)
        if option3:
            return (False,False,True,False)
        if option4:
            return (False,False,False,True)
    else:
        return (False,False,False,False)



    

    

