import pygame, sys
from character import *
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
            
    if player._gety() <= 200:
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
    if len(action_queue) > 2:
        current_move = action_queue[0]
        mode = ""

        #so that the program skips default:
        next_in = 1
        while action_queue[next_in].get_name() == "default": #or action_queue[next_in].get_name() == action_queue[next_in - 1].get_name():
            next_in += 1
            if next_in > len(action_queue):
                next_in = 1
                break
            break
        check_move = action_queue[next_in]

        #check_move = previous_move


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

            if len(action_queue) > 0:
                action_queue.remove(action_queue[0])
            mode = current_move.get_mode()

        #if there is a combination of an attacking key and a movement key: - this works a bit
        if not current_move.get_movement() and check_move.get_movement() or current_move.get_movement() and not check_move.get_movement():
            if current_move.get_name() != "default" or check_move.get_name() != "default":# or previous_move.get_name() != current_move.get_name():
                
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
                        player.low_kick()

                    if check_move.get_name() == "block":
                        player.low_block()
                for x in range(2):
                    if len(action_queue) > 0:
                        action_queue.remove(action_queue[0])
                mode = ""
                
        if not player.get_animating() or current_move.get_name() == "default":
            if player.get_default_mode():
                #^ to make sure that the first frame isn't reset
                pass
            else:
                player.default()
                player._sety(275)
            if len(action_queue) > 0:
                action_queue.remove(action_queue[0])
            
        action_queue = []
        return mode, action_queue

    else:
        if not player.get_animating():
            if player.get_default_mode():
                #^ to make sure that the first frame isn't reset
                pass
            else:
                player.default()
                #player._sety(275)
        return "", action_queue         

def set_positions(player):
    player._setx(300)
    player._sety(275) 
    player.set_health(100)
    player.set_attack_power(5)
    player.default()
    

play = True
screen = pygame.display.set_mode((400,400),0,32)
player = load_character("Goku", screen)
characters = [player]
group = add_group(characters)
player._setx(0)
player._sety(275)
player.default()
framerate = pygame.time.Clock()
moves = set_move()
action_queue = []

while play:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    action_queue = set_queue(action_queue, moves, player)

    if not player.get_animating():
        tuple1 = player_reaction2(player, action_queue)
        mode = tuple1[0]
        action_queue = tuple1[1]
##        for x in action_queue:
##            print(x.get_name())
    
    screen.fill((255,255,255))
    player.update(ticks, 180, player._getx(), player._gety(), mode)
    group.draw(screen)
    
    pygame.display.update()

    
    

