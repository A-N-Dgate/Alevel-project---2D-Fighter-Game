import pygame, sys
from characterV3 import *

objectives= """
---hold down key for:
       right/left
       crouch
       block
       ^
       ---complete---
       
---jump and direction
    ^wont work without combination keys work
---combination key recognision working
    ^impossible :)
"""

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

       

def set_positions(player):
    player._setx(300)
    player._sety(275) 
    player.set_health(100)
    player.set_attack_power(5)
    player.default()

#--------------------------------------------------------------------------------------------------------------
def keydown_check(user_input, keydown):
    keydown1, keydown2, k3, k4 = keydown
    if user_input[K_z]:
        keydown1 = True
    else:
        keydown1 = False

    if user_input[K_DOWN]:
        keydown2 = True
    else:
        keydown2 = False

    if user_input[K_RIGHT]:
        k3 = True
    else:
        k3 = False

    if user_input[K_LEFT]:
        k4 = True
    else:
        k4 = False

    return keydown1, keydown2, k3, k4


def check_true(keydown):
    #so that one boolean value is passed into the update method
    for boolean in keydown:
        if boolean == True:
            return True
    return False
    


def check_queue(action_queue):
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

    return current_move, check_move

def combination_move_check(current_move, check_move, player, action_queue):
    if not current_move.get_movement() and check_move.get_movement() or current_move.get_movement() and not check_move.get_movement():
        #check each combination
        if check_move.get_name() == "jump":
            if current_move.get_name() == "punch":
                player.uppercut()

            if current_move.get_name() == "kick":
                player.high_kick()

#---------------highest point doesn't work-------------------------
            if player.get_highest_point():
                #print("check1")
                if current_move.get_name() == "right":
                    #print("check2")
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
            if check_move.get_name() == "punch":
                player.uppercut()

            if check_move.get_name() == "kick":
                player.high_kick()

            if player.get_highest_point():
                #print("check1")
                #^ this is printed at the worng time...
                if check_move.get_name() == "right":
                    #print("check2")
                    if player.get_reversed():
                        player.move_left()
                    else:
                        player.move_right()

                if check_move.get_name() == "left":
                    if player.get_reversed():
                        player.move_right()
                    else:
                        player.move_left()

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
        action_queue = []
        #^since the character will perform an extra move after the combination move

        return action_queue, mode

def single_move_check(current_move, player, action_queue):
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

    return action_queue, mode


def default_check(current_move, player, action_queue):
    if not player.get_animating() or current_move.get_name() == "default":
        if player.get_default_mode():
            #^ to make sure that the first frame isn't reset
            pass
        else:
            player.default()
            if player.get_in_air():
                pass
            else:
                player._sety(player.get_default_y())
                #^so that he y vlaue isnt set to defualt while the player is falling

        if len(action_queue) > 0:
            action_queue.remove(action_queue[0])

    return action_queue

def player_reaction3(player, action_queue):
    mode = ""
    current_move, check_move = check_queue(action_queue)
    actionqueue_mode = None

    if current_move == "":
        return "", action_queue
    
##    #---testing---
##    for x in action_queue:
##        if x.get_name() == "default":
##            pass
##        else:
##            print(x.get_name())
##            print("---------------------")
##    #-------------

    if check_move != None:
        actionqueue_mode = combination_move_check(current_move, check_move, player, action_queue)

    if actionqueue_mode != None:
        action_queue, mode = actionqueue_mode
    else:
        action_queue, mode = single_move_check(current_move, player, action_queue)

    action_queue = default_check(current_move, player, action_queue)

    if len(action_queue) > 4:
        action_queue = []
        #^failsafe: to stop the queue from being stuck on one move, freezing the game

    return mode, action_queue

pygame.init()
screen = pygame.display.set_mode((997,500),0,32)
pygame.display.set_caption("Test - Player Reaction")

player = Goku(screen)
group = pygame.sprite.Group()
group.add(player)
player._setx(0)
player._sety(player.get_default_y())
player.default()

framerate = pygame.time.Clock()
moves = set_move()
action_queue = []

#---
keydown = (False, False, False, False) 
#---

while True:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    action_queue, keydown = set_queue(action_queue, moves, player, keydown)
    keypressed = check_true(keydown)

    if not player.get_animating():
        mode, action_queue = player_reaction3(player, action_queue)

    
    screen.fill((255,255,255))
    player.update(ticks, 180, player._getx(), player._gety(), mode, keypressed)
    group.draw(screen)
    
    pygame.display.update()

    
    

