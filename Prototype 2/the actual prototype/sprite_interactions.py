import pygame, sys
from character import *
from update_display import *
from character import *

#------------------all---------------------------

def exit_game():
    pygame.quit()
    sys.exit()

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


def set_move():
    punch = action("punch", False, False, "")
    block = action("block", False, False, "")
    chop = action("chop", False, False, "")
    kick = action("kick", False, False, "")
    jump = action("jump", True, True, "jump")
    crouch = action("crouch", True, False, "")
    right = action("right", True, True, "right")
    left = action("left", True, True, "left")
    down = action("down", True, True, "down")
    default = action("default", False, False, "")

    return (punch, block, chop, kick, jump, crouch, right, left, down, default)


def set_queue(action_queue, moves, player):  
#punch, block, chop, kick, jump, crouch, right, left, down, default

    action_queue.reverse()
    action_taken = moves[9]

    for event in pygame.event.get():
        user_input = pygame.key.get_pressed()
        if event.type == QUIT:
            exit_game()
        
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

    if len(player.values) != 0:
        if player._gety() <= player.get_highest_y(): 
            action_taken = moves[8]


    try:
        if action_queue[0].get_name() != action_taken.get_name():
            action_queue.append(action_taken)
    except: #queue too small to check
        action_queue.append(action_taken)
            
    action_queue.reverse()
    return action_queue

def player_reaction(player, action_queue):   
    mode = ""
    if len(action_queue) > 1:
        current_move = action_queue[0]

        #so that the program skips default:
        next_in = 1
        try:
            while action_queue[next_in].get_name() == "default": 
                next_in += 1
        except: #list is too small
            next_in = 1
        check_move = action_queue[next_in]


    elif len(action_queue) <= 1:
        current_move = action_queue[0]
        check_move = None

    else: #nothing in the queue
        return "", action_queue

   

    if check_move != None:
        if not current_move.get_movement() and check_move.get_movement() or current_move.get_movement() and not check_move.get_movement():
            if current_move.get_name() != "default" or check_move.get_name() != "default":
                if check_move.get_name() == "jump":
                    if current_move.get_name() == "punch":
                        player.uppercut()

                    if current_move.get_name() == "kick":
                        player.high_kick()

                if current_move.get_name() == "jump":
                    if check_move.get_name() == "punch":
                        player.uppercut()

                    if check_move.get_name() == "kick":
                        player.high_kick()

                if check_move.get_name() == "crouch":
                    if current_move.get_name() == "punch":
                        player.low_punch()

                    if current_move.get_name() == "kick":
                        player.low_kick()

                    if current_move.get_name() == "block":
                        player.low_block()

                if current_move.get_name() == "crouch":
                    if check_move.get_name() == "punch":
                        player.low_punch()

                    if check_move.get_name() == "kick":
                        player.low_kick()

                    if check_move.get_name() == "block":
                        player.low_block()

                if not player.get_default_mode():
                    move_found = True
            mode = ""
            
     #if there isnt a second move to check
    if current_move != None and check_move == None:
        if not current_move.get_movement():
            if current_move.get_name() == "punch":
                player.punch()
                
            if current_move.get_name() == "kick":
                player.kick()

            if current_move.get_name() == "chop":
                player.chop()

            if current_move.get_name() == "block":
                player.block()
            if len(action_queue) > 0:
                action_queue.remove(action_queue[0])

        if current_move.get_movement():
            if current_move.get_name() == "right":
                if player.get_reversed():
                    player.move_left()
                else:
                    player.move_right()

            if current_move.get_name() == "left":
                if player.get_reversed():
                    player.move_right()
                else:
                    player.move_left()

            if current_move.get_name() == "jump":
                player.jump()

            if current_move.get_name() == "crouch":
                player.crouch()

            if current_move.get_name() == "down":
                player.back_down()

        mode = current_move.get_mode()
                        
    if not player.get_animating() or current_move.get_name() == "default":
        if player.get_default_mode():
            #^ to make sure that the first frame isn't reset
            pass
        else:
            player.default()
            if player.in_air: 
                pass
            else:
                player._sety(player.get_default_y())

    if len(action_queue) > 0:
        action_queue.remove(action_queue[0])

    #print(action_queue)
    action_queue = []
    return mode, action_queue



def check_attacks(player, enemy):
    if player.get_attacking():
        enemy.check_attack(player)

    if enemy.get_attacking():
        player.check_attack(enemy)



#------------------character selection---------------
    
def select_eventcheck():
    x = y = 0
    for event in pygame.event.get():
        if event.type == QUIT:
            exit_game()

        if event.type == MOUSEBUTTONUP:
            x,y = pygame.mouse.get_pos()


    return x,y


def check_click(select,x,y):
    player = None
    option1 = select[0].check_click(x,y)
    option2 = select[1].check_click(x,y)
    option3 = select[2].check_click(x,y)

    if option1 != None or option2 != None or option3 != None:
        if option1 != None:
            player = option1
        if option2 != None:
            player = option2
        if option3 != None:
            player = option3

    return  player


    

