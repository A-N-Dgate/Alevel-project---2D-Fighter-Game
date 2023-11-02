import pygame, os, sys
from pygame.locals import *
from select_sprites import *      

pygame.init()
screen = pygame.display.set_mode((997,473))
pygame.display.set_caption("Test - main menu")
framerate = pygame.time.Clock()

background_path = os.path.join("spritesheets", "backgrounds", "menu_background.png")
background = pygame.image.load(background_path)

image_path = os.path.join("spritesheets", "select_sprites", "test_select3.png")
arcade_path = os.path.join("spritesheets", "select_sprites", "arcade.png")
exit_path = os.path.join("spritesheets", "select_sprites", "exit.png")
practice_path = os.path.join("spritesheets", "select_sprites", "practice_mode.png")
controls_path = os.path.join("spritesheets", "select_sprites", "controls.png")

arcade_mode = menu_select_sprite(screen, arcade_path, 445, 220, 133,38)
controls = menu_select_sprite(screen, controls_path, 412,330 , 183, 38)
practice_mode = menu_select_sprite(screen, practice_path, 420, 277 , 171, 38)
exit_select = menu_select_sprite(screen, exit_path, 465, 381,83, 38)

group = pygame.sprite.Group()
group.add(arcade_mode)
group.add(controls)
group.add(exit_select)
group.add(practice_mode)

selected_mode = False
option1 = None
option2 = None
option3 = None
option4 = None
x = y = 0


while not selected_mode:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == MOUSEBUTTONUP:
            option1 = arcade_mode.check_click(x,y)
            option2 = controls.check_click(x,y)
            option3 = exit_select.check_click(x,y)
            option4 = practice_mode.check_click(x,y)

        if event.type == MOUSEMOTION:
            x,y = pygame.mouse.get_pos()

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if option1 or option2 or option3 or option4:
        print("mode selected")
        if option1:
            print("arcade mode selected")
        if option2:
            print("controls screen selected")
        if option3:
            print("exit game slected")
        if option4:
            print("practice mode selected")
        selected_mode = True
    


    screen.blit(background, (0,0))
    group.update(x,y)
    group.draw(screen)

    pygame.display.update()

pygame.quit()
sys.exit()
