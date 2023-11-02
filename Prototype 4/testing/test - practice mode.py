import pygame, sys, os
from characterV4 import *
from level_top_display import *
from character_responce import *
from action_classes import *
from select_sprites import *


##def get_queue_images(queue):
##    image_list = []
##    for item in queue:
##        if item.get_name() != "default" or item.get_name() != "back_down":
##            path = os.path.join("spritesheets", "practice_mode", "%s.png" %(item.get_name()))
##            image = pygame.image.load(path)
##            image_list.append(image)
##
##    return image_list

def get_queue_images(queue):
    image_list = []
    for item in queue:
        try:
            path = os.path.join("spritesheets", "practice_mode", "%s.png" %(item.get_name()))
            image = pygame.image.load(path)
            image_list.append(image)
        except: #image doesn't exist
            pass
    return image_list

def display_queue(screen, queue, previous_list):
    image_list = get_queue_images(queue)
    image_list.reverse()
    if len(image_list) == 0:
        image_list = previous_list
    for image in image_list:
        screen.blit(image, (10, (40 +(20* image_list.index(image)))))
    return image_list


def setqueue_eventcheck(action_queue, moves, player, keydown, exit_game, mouse_x, mouse_y):  
#punch, block, chop, kick, jump, crouch, right, left, down, default

    action_queue.reverse()
    action_taken = moves[9]

    for event in pygame.event.get():
        user_input = pygame.key.get_pressed()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    #---------------------------practice mode event check -----------------------
        if event.type == MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()

        if event.type == MOUSEBUTTONUP:
            exit_game = exit_select.check_click(mouse_x, mouse_y)
    #----------------------------------------------------------------------------
        
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
    return action_queue, keydown, exit_game,mouse_x, mouse_y




pygame.init()
screen = pygame.display.set_mode((997,473))
pygame.display.set_caption("test - practoce mode")

#player set up
player = Goku(screen)
#in the prototype, the user will select a character
player._setx(10)
player._sety(player.get_default_y())
player.default()
player.set_health_bar(health_bar(player, screen, False))

#dummy set up
dummy = Goku(screen)
dummy._setx(800)
dummy._sety(dummy.get_default_y())
dummy.set_bool_reversed(True)
dummy.default()
dummy.set_health_bar(health_bar(dummy, screen, True))

#characters set up
group = pygame.sprite.Group()
group.add(player)
group.add(dummy)

healthbar_group = pygame.sprite.Group()
healthbar_group.add(player.get_health_bar())
healthbar_group.add(dummy.get_health_bar())

#game set up
moves = set_move()
action_queue = []
keydown = [False, False, False, False]
framerate = pygame.time.Clock()

previous_list = []
exit_game = False

#exit button set up
exit_path = os.path.join("spritesheets", "select_sprites", "exit.png")
x = 455
y = 10
exit_select = menu_select_sprite(screen, exit_path, x,y,83, 38)
button_group = pygame.sprite.Group()
button_group.add(exit_select)
mouse_x = mouse_y = 0


while True:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    action_queue, keydown, exit_game, mouse_x, mouse_y = setqueue_eventcheck(action_queue, moves, player, keydown, exit_game, mouse_x, mouse_y)
    keypressed = check_true(keydown)


    if not player.get_animating():
        mode, action_queue = character_reaction4(player, action_queue)

    #---------dummy reaction - need a procedure in sprite interations-----------

    if not dummy.get_animating():
        if dummy.get_default_mode():
            pass
        else:
            dummy.default()

    if player.get_attacking():
        dummy.check_attack(player) 

    if dummy.get_health() <= 0:
        dummy.set_health(dummy.get_original_health())

    #----------------------------------------------------------------------------

    screen.fill((255,255,255))
    player.set_reversed(dummy)
    player.update(ticks, 180, player._getx(), player._gety(), mode, keypressed)
    dummy.set_reversed(player)
    dummy.update(ticks, 180, dummy._getx(), dummy._gety(), "", False)
    healthbar_group.update()
    healthbar_group.draw(screen)
    exit_select.update(mouse_x, mouse_y)
    button_group.draw(screen)
    group.draw(screen)

    previous_list = display_queue(screen, action_queue, previous_list)

    pygame.display.update()

    if exit_game:
        pygame.quit()
        sys.exit()
    

            
    
                     


