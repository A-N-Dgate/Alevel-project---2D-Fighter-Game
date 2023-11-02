import pygame, sys, time, os
from character import *
from import_file import *

#set up pygame
pygame.init()
screen = pygame.display.set_mode((400,400),0,32)
pygame.display.set_caption("Character Animation")

framerate = pygame.time.Clock()

#create sprite
player = character("Goku", screen)
path = os.path.join("spritesheets", "Goku", "GokuSheet.png")
player.load(path, 95, 110, 75)
group = pygame.sprite.Group()
group.add(player)

#change move here: (except for default)
player.high_kick() 

def check_mode():
    if not player.get_animating():
        pygame.quit()
        sys.exit()

while True:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        pygame.quit()
        sys.exit()

    check_mode()
    screen.fill((0,0,255))
    player.update(ticks,260,0,0)
    print_text(screen, 0, 0, str(player))
    group.draw(screen)
    
    pygame.display.update()
