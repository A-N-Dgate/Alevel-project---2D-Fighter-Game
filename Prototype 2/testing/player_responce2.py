import pygame, sys
from characterV2 import *
from set_up import *

class action():
    def __init__(self, name, movement, has_mode, mode):
        self.name = name
        self.mode = mode
        #boolean values
        self.movement = movement
        self.has_mode = has_mode

    #set once so it doesn't need set methods
    def get_name(self): return self.name
    def get_movement(self): return self.movement
    def get_has_mode(self): return self.has_mode
    def get_mode(self): return self.mode

          
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

    if len(player.values) != 0:
        if player._gety() <= player.values[1]: #write a get_values method
            action_taken = moves[8]


    try:
        if action_queue[0].get_name() != action_taken.get_name():
            action_queue.append(action_taken)
    except: #queue too small to check
        action_queue.append(action_taken)
            
    #print("%s, movement: %s" %(action_taken.get_name(), action_taken.get_movement()))

            
    action_queue.reverse()
    return action_queue

def player_reaction2(player, action_queue):
##    #boundary check:
##    if player._gety() < 0:
##        player._sety(275)
        
    mode = ""
#----------------------------------------------------------------------------
    if len(action_queue) > 1:
        current_move = action_queue[0]

        #so that the program skips default:
        next_in = 1
        try:
            while action_queue[next_in].get_name() == "default": #or action_queue[next_in].get_name() == action_queue[next_in - 1].get_name():
                next_in += 1
        except: #list is too small
            next_in = 1
        check_move = action_queue[next_in]

        #check_move = previous_move
##        check_move = None
##        next_in = 0

    elif len(action_queue) <= 1:
        current_move = action_queue[0]
        check_move = None

    else: #nothing in the queue
        return "", action_queue
#----------------------------------------------------------------------------
##^check_queue function

    #print(current_move, check_move)
        
   

    if check_move != None:# and current_move != None: 
##        move_found = False
##        next_in = 0
##        while not move_found:
##            try:
##                next_in += 1
##                while action_queue[next_in].get_name() == "default":
##                    next_in += 1
##                check_move = action_queue[next_in]
##                
##            except: #no more moves to check 
##                move_found = True
                
            ##print("\ncurrent move : %s \ncheck move : %s \n\n" %(current_move.get_name(), check_move.get_name()))
            #if there is a combination of an attacking key and a movement key
        
        if not current_move.get_movement() and check_move.get_movement() or current_move.get_movement() and not check_move.get_movement():
            if current_move.get_name() != "default" or check_move.get_name() != "default":#  or previous_move.get_name() != current_move.get_name():
                #^ still checks default
                #check each combination
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
                        #print("check2")
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
                #print("check3")
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
            if player.in_air: #write a get method
                pass
            else:
                try:
                    player._sety(player.values[0])
                except:
                    player._sety(275)

    if len(action_queue) > 0:
        action_queue.remove(action_queue[0])

    #print(action_queue)
    action_queue = []
    return mode, action_queue
       
