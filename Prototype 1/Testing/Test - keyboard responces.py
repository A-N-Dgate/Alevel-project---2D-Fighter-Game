import pygame, os, sys
from character import *
from import_file import *


#set up pygame
pygame.init()
screen = pygame.display.set_mode((400,400),0,32)
pygame.display.set_caption("Keyboard responces")
framerate = pygame.time.Clock()

#create sprite
player = character("Goku", screen)
path = os.path.join("spritesheets", "Goku", "GokuSheet.png")
player.load(path, 95, 110, 75)
group = pygame.sprite.Group()
group.add(player)

#set position of player
player.default()
mode = ""
player._setx(0)
player._sety(275) 


while True:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        user_input = pygame.key.get_pressed()

        #combination keys first - these don't work
        if user_input[K_a] and user_input[K_DOWN]:
            player.low_punch()

        if user_input[K_x] and user_input[K_DOWN]:
            player.low_kick()

        if user_input[K_z] and user_input[K_DOWN]:
            player.low_block()

        if user_input[K_a] and user_input[K_UP]:
            player.uppercut()

        if user_input[K_x] and user_input[K_UP]:
            player.high_kick()

        #single keys
        if user_input[K_a]:
            player.punch()

        if user_input[K_z]:
            player.block()

        if user_input[K_s]:
            player.chop()

        if user_input[K_x]:
            player.kick()

        #directional keys
        if user_input[K_UP]:
            player.jump()
            mode = "jump"
        
        if user_input[K_DOWN]:
            player.crouch()

        if user_input[K_RIGHT]:
            player.move_right()
            mode = "right"

        if user_input[K_LEFT]:
            player.move_left()
            mode = "left"

        
    #making sure the player stays on screen
    if player._gety() < 0 :
        player._sety(300)

    if player._getx() > 330 or player._getx() < 0:
        player._setx(0)

    #and gravity
    if player._gety() <= 223:
        player.back_down()
        mode = "down"
                    
    #if the player isn't doing anything:
    if not player.get_animating():
        if player.get_default_mode():
            #^ to make sure that the first frame isn't reset
            pass
        else:
            player.default()
            mode = ""

    screen.fill((0,0,255))
    pygame.draw.rect(screen, (255,0,0), player.get_hitbox(), 5)
    player.update(ticks, 180, player._getx(), player._gety(), mode)
    group.draw(screen)
    print_text(screen, 0, 0, str(player))
    
    pygame.display.update()
            
            
            
        
            

        
        
        
        
                          
        
        
        
