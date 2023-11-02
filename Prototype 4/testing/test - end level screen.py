import pygame, sys, os
from characterV4 import *

pygame.init()
screen = pygame.display.set_mode((997,473))
pygame.display.set_caption("test - end level screen")

win = True
#^change boolean to test each scenario
player = Goku(screen)

#setup player icon
player.get_icon().set_outcome(win)

#make an instance of each enemy to use thier icon
level1 = Raditz(screen)
level2 = Frieza(screen)
level3 = Trunks(screen)
level4 = Vegeta(screen)
#^for testing

#set images for each
player.get_icon().set_image()
level1.get_icon().set_image()
level2.get_icon().set_image()
level3.get_icon().set_image()
level4.get_icon().set_image()

#set x and y positions of each icon
level1.get_icon()._setpos((500,350))
level2.get_icon()._setpos((500,250))
level3.get_icon()._setpos((500,150))
level4.get_icon()._setpos((500,50))
player.get_icon()._setpos((400,level1.get_icon()._gety()))

#set rects for the enemy icons
level1.get_icon().set_rect_enemy()
level2.get_icon().set_rect_enemy()
level3.get_icon().set_rect_enemy()
level4.get_icon().set_rect_enemy()

#add to sprite group
group = pygame.sprite.Group()
group.add(player.get_icon())
group.add(level1.get_icon())
group.add(level2.get_icon())
group.add(level3.get_icon())
group.add(level4.get_icon())


background = pygame.image.load(os.path.join("spritesheets", "backgrounds", "end_level_background.png"))

framerate = pygame.time.Clock()
stop_animating = False
#^changed by returning the icon update

while not stop_animating:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background, (0,0))
    stop_animating = player.get_icon().update(ticks, 180, level2)
    group.draw(screen)

    pygame.display.update()

if stop_animating:
    if win:
        print("next level")
        pygame.quit()
        sys.exit()
    else:
        print("main menu")
        pygame.quit()
        sys.exit()

    

