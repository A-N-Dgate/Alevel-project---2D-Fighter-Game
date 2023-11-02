import pygame, os, sys
from select_sprites import *
from characterV5 import *

pygame.init()
screen = pygame.display.set_mode((997,473))
pygame.display.set_caption("Test - character select screen")
background = pygame.image.load(os.path.join("spritesheets", "backgrounds", "char_select_background.png"))

#menu seelct sprites
extra_path = os.path.join("spritesheets", "select_sprites", "extra.png")
back_path = os.path.join("spritesheets", "select_sprites" , "back.png")
extra_button = menu_select_sprite(screen, extra_path,450,60,116,38)
back_button = menu_select_sprite(screen, back_path, 460, 60,91,38)
#don't put them in a group together bc they will be on seperate screens
extra_group = pygame.sprite.Group()
extra_group.add(extra_button)
back_group = pygame.sprite.Group()
back_group.add(back_button)


#character select sprites - raditz unlocked = True only
r_path = os.path.join("spritesheets", "select_sprites", "select_raditz.png")
f_path = os.path.join("spritesheets", "select_sprites", "select_frieza.png")
c_path = os.path.join("spritesheets", "select_sprites", "select_cell.png")

#draw characters on screen to find the select x values
raditz = Raditz(screen)
frieza = Frieza(screen)
cell = Cell(screen)

select_raditz = unlockable_character_select_sprite(screen, raditz, r_path,25,110, True)
select_frieza = unlockable_character_select_sprite(screen, frieza, f_path, 350, 110, False)
select_cell = unlockable_character_select_sprite(screen, cell, c_path, 675, 110, False)

unlockable_group = pygame.sprite.Group()
unlockable_group.add(select_raditz)
unlockable_group.add(select_frieza)
unlockable_group.add(select_cell)


#values
def main_char_select():
    framerate = pygame.time.Clock()
##    main_select = True
##    unlockable_select = False
    x = y = 0
    go_back = False
    option1 = None
    option2 = None
    option3 = None

    while True:
        framerate.tick(30)
        ticks = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                x,y = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                next_page = extra_button.check_click(x,y)
                if next_page:
##                    main_select = False
##                    unlockable_select = True
                    next_screen()
                    


        #update
        screen.blit(background, (0,0))
        extra_button.update(x,y)
        extra_group.draw(screen)

        pygame.display.update()

def next_screen():
    x = y = 0
    go_back = False
    option1 = None
    option2 = None
    option3 = None
    framerate = pygame.time.Clock()

    #character set up
    raditz.default()
    raditz._setx(raditz.get_select_x())
    raditz._sety(raditz.get_default_y())

    frieza.default()
    frieza._setx(frieza.get_select_x())
    frieza._sety(frieza.get_default_y())

    cell.default()
    cell._setx(cell.get_select_x())
    cell._sety(cell.get_default_y())

    group = pygame.sprite.Group()
    group.add(raditz)
    group.add(frieza)
    group.add(cell)
    
    while True:
        framerate.tick(30)
        ticks = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                x,y = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                if select_raditz.get_character_unlocked():
                    option1 = select_raditz.check_click(x,y)

                if select_frieza.get_character_unlocked():
                    option2 = select_frieza.check_click(x,y)

                if select_cell.get_character_unlocked():
                    option3 = select_cell.check_click(x,y)

                #could make a function: pass in a select sprite
                # and return None if not unlocked, and True or
                #False if clicked

                go_back = back_button.check_click(x,y)
                
        if option1 != None or option2 != None or option3 != None:
            if option1 != None:
                print("raditz selected")
            if option2 != None:
                print("frieza selected")
            if option3 != None:
                print("cell selected")
            pygame.quit()
            sys.exit()

        if go_back:
            main_char_select()
            #go back to the main character select screen

        #update

        screen.blit(background, (0,0))
        back_button.update(x,y)
        unlockable_group.update(x,y)
        raditz.update(ticks, 180, raditz._getx(), raditz._gety(), "", False)
        frieza.update(ticks, 180, frieza._getx(), frieza._gety(), "", False)
        cell.update(ticks, 180, cell._getx(), cell._gety(), "", False)
        back_group.draw(screen)
        unlockable_group.draw(screen)
        group.draw(screen)

        pygame.display.update()
        
            
main_char_select()       
    

        
    




