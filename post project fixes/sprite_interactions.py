import pygame, sys
from character import *
from update_display import *
from character import *
from character_extras import *
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

def event_check():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit_game()
            

#------------------levels------------------------
def stay_on_screen(player, enemy):
    if player._getx() < 0:
        player._setx(0)

    if enemy._getx() < 0:
        enemy._setx(0)

    if player._getx() > 900:
        player._setx(900)

    if enemy._getx() > 900:
        enemy._setx(900)


def dummy_reaction(dummy):
    if not dummy.get_animating():
        if dummy.get_default_mode():
            pass
        else:
            dummy.default()

def level_event_check():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit_game()




def set_stack(action_stack, moves, player, keydown):  
#punch, block, chop, kick, jump, crouch, right, left, down, default

    action_stack.reverse()
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
        if action_stack[0].get_name() != action_taken.get_name():
            action_stack.append(action_taken)
    except: #queue too small to check
        action_stack.append(action_taken)
            
    action_stack.reverse()
    return action_stack, keydown

def keydown_check(user_input, keydown):
    k1, k2, k3, k4 = keydown
    if user_input[K_z]:
        k1 = True
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


def get_check_move(next_in, action_stack):
    try:
        while action_stack[next_in].get_name() == "default" and action_stack[next_in].get_name() == action_stack[next_in + 1].get_name(): 
            next_in += 1
        return action_stack[next_in]
    except:
        return None

    

def check_stack(action_stack):
    if len(action_stack) > 1:
        current_move = action_stack[0]

        check_move1 = get_check_move(1, action_stack)
        check_move2 = get_check_move(2,action_stack)

        return current_move, check_move1, check_move2
        
    elif len(action_stack) == 1:
        current_move = action_stack[0]
        check_move1 = None
        check_move2 = None

    else: #nothing in the queue
        return "", action_stack

    return current_move, check_move1, check_move2

def combination_move_check(current_move, check_move, character, action_stack):
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
                character.low_block()

        if current_move.get_name() == "crouch":
            if check_move.get_name() == "punch":
                character.low_punch()

            if check_move.get_name() == "kick":
                character.low_kick()

            if check_move.get_name() == "block":
                character.low_block()
            
        mode = ""
        action_stack = []
        #^since the character will perform an extra move after the combination move

        return action_stack, mode

def single_move_check(current_move,check_move, character, action_stack):
    move_taken = False
    
    if current_move.get_name() == "default":
        return action_stack, ""            
         
    if current_move.get_name() == "move_right" and character.get_reversed():
        action_method = getattr(character, "move_left")
        action_method()
    elif current_move.get_name() == "move_left" and character.get_reversed():
        action_method = getattr(character, "move_right")
        action_method()
    else:
        action_method = getattr(character, current_move.get_name())
        action_method()

    mode = current_move.get_mode()
    move_taken = True

    if not move_taken:
        #the check move won't be default, but the current move can be
        if (current_move.get_name() == "right" or current_move.get_name() == "left") and character.get_reversed():
            if current_move.get_name() == "right":
                action_method = getattr(character, "left")
                action_method()
            elif current_move.get_name() == "left":
                action_method = getattr(character, "right")
                action_method()
        else:
            action_method = getattr(character, current_move.get_name())
            action_method()

    if len(action_stack) > 0:
        action_stack.remove(action_stack[0])
    return action_stack, mode

def default_check(character, action_stack):
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

        if len(action_stack) > 0:
            action_stack.remove(action_stack[0])

    return action_stack

def special_move_check(current_move, check_move1, check_move2, character, action_stack):
    if check_move1 == None or check_move2 == None:
        return None
    move_list = [check_move2.get_name(), check_move1.get_name(), current_move.get_name()]
    for special_move in character.get_special_moves():
        action_list = character.get_special_moves()[special_move]
        if action_list == move_list:
            action_taken = getattr(character, special_move)
            action_taken()
            action_stack = []
            return action_stack, ""

def character_reaction(character, action_stack):
    mode = ""
    current_move, check_move1, check_move2 = check_stack(action_stack)
    actionqueue_mode = None

    if current_move == "":
        return "", action_stack

    action_mode = special_move_check(current_move, check_move1, check_move2, character, action_stack)
    if check_move1 != None and action_mode == None:
        action_mode = combination_move_check(current_move, check_move1, character, action_stack)

    if action_mode != None:
        action_stack, mode = action_mode
    else:
        action_stack, mode = single_move_check(current_move,check_move1, character, action_stack)

    action_stack = default_check(character, action_stack)

    if len(action_stack) > 4:
        action_stack = []
        #^failsafe: to stop the stack from being stuck on one move, freezing the game

    return mode, action_stack



def check_attacks(player, enemy):
    if player.get_attacking():
        enemy.check_attack(player)

    if enemy.get_attacking():
        player.check_attack(enemy)



#------------------character selection---------------
    
def select_eventcheck(x,y,sprites):
    item_list = []
    
    for event in pygame.event.get():
        all_mouse_buttons = pygame.mouse.get_pressed()
        if event.type == QUIT:
            exit_game()

        if event.type == MOUSEMOTION:
            x,y = pygame.mouse.get_pos()

        if all_mouse_buttons[0] or all_mouse_buttons[2]:
            for sprite in sprites:
                item = sprite.check_click(x,y)
                item_list.append(item)

    return x,y, item_list


def character_select_checkclick(option1,option2,option3,option4):
    player = None
    switch = False

    if option4:
        switch = True

    elif option1 != None or option2 != None or option3 != None:
        if option1 != None:
            player = option1
        if option2 != None:
            player = option2
        if option3 != None:
            player = option3
        switch = False


    return  player, switch

#------------------main menu---------------------

def menu_checkclick(option1,option2,option3,option4):
# return booleans(arcade,practice,controls,exit)
    if option1 or option2 or option3 or option4:
        if option1:
            return (True,False,False,False)
        if option2:
            return (False,False,True,False)
        if option3:
            return (False,True,False,False)
        if option4:
            return (False,False,False,True)
    else:
        return (False,False,False,False)



#------------------Practice mode---------------------

def setqueue_eventcheck(action_stack, moves, player, keydown, exit_game,exit_select, mouse_x, mouse_y):  
#punch, block, chop, kick, jump, crouch, right, left, down, default

    action_stack.reverse()
    action_taken = moves[9]

    for event in pygame.event.get():
        user_input = pygame.key.get_pressed()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()

        if event.type == MOUSEBUTTONUP:
            exit_game = exit_select.check_click(mouse_x, mouse_y)
        
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
        if action_stack[0].get_name() != action_taken.get_name():
            action_stack.append(action_taken)
    except: #queue too small to check
        action_stack.append(action_taken)
            
    action_stack.reverse()
    return action_stack, keydown, exit_game,mouse_x, mouse_y


def check_attack_dummy(player, dummy):
    if player.get_attacking():
        dummy.check_attack(player)

    if dummy.get_health() <= 0:
        dummy.set_health(dummy.get_original_health())



#----------------------controls --------------------------

def back_button_click_check(x,y,back_button):
    x,y,back = select_eventcheck(x,y,[back_button])
    #^as a list

    if True in back:
        return x,y,True
    else:
        return x,y,False


#-----------------------load data ------------------------------

def enter_name_event_check(enter, letters):
    #using pygame key and event functions 
    for event in pygame.event.get():
        if event.type == QUIT:
            exit_game()

        if event.type == KEYDOWN:
            if event.key == pygame.K_RETURN:
                pygame.mixer.Channel(2).play(pygame.mixer.Sound(os.path.join("sfx", "select.wav")))
                enter = True

            elif len(pygame.key.name(event.key)) > 1:
                #check backspace
                if event.key == pygame.K_BACKSPACE:
                    try:
                        letters.pop()
                    except IndexError:
                        pass

            else:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join("sfx", "mouse_on.wav")))
                letters.append(pygame.key.name(event.key))

    return enter,letters


def set_name(letters, player_name):   
    for letter in letters:
        player_name += letter

    return player_name


def load_check_click(options):
    if len(options) == 0 or True not in options:
        return False, False
    elif len(options) == 2:
        return options
    
    

    

        





    

    

