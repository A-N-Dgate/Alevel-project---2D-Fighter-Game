import pygame, sys, os
from select_sprites import *
from characterV3 import *

pygame.init()
screen = pygame.display.set_mode((997,473),0,32)
frame_rate = pygame.time.Clock()
frame_rate.tick(30)

goku = Goku(screen)
vegeta = Vegeta(screen)
trunks = Trunks(screen)

goku.default()
vegeta.default()
trunks.default()

gx, gy =(goku.get_select_x(), goku.get_default_y()) 
vx, vy = (vegeta.get_select_x(), vegeta.get_default_y())
tx, ty = (trunks.get_select_x(), trunks.get_default_y())

goku._setpos((gx, gy))
vegeta._setpos((vx, vy))
trunks._setpos((tx, ty))

background_path = os.path.join("spritesheets", "backgrounds", "char_select_background.png")
background = pygame.image.load(background_path)

image_path = os.path.join("spritesheets", "select_sprites", "test_image4.png")
goku_path = os.path.join("spritesheets", "select_sprites", "select_goku.png")
trunks_path = os.path.join("spritesheets", "select_sprites", "select_trunks.png")
vegeta_path = os.path.join("spritesheets", "select_sprites", "select_vegeta.png")

select_goku = character_selection_sprite(screen, goku,goku_path, 25,110) 
select_vegeta = character_selection_sprite(screen, vegeta,vegeta_path, 350, 110)
select_trunks = character_selection_sprite(screen, trunks,trunks_path, 675,110)

character_group = pygame.sprite.Group()
character_group.add(goku)
character_group.add(vegeta)
character_group.add(trunks)

select_group = pygame.sprite.Group()
select_group.add(select_goku)
select_group.add(select_vegeta)
select_group.add(select_trunks)

player = None
option1 = None
option2 = None
option3 = None

player_added = False
x = y = 0

while not player_added:
    frame_rate.tick(30)
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == MOUSEMOTION:
            x,y = pygame.mouse.get_pos()
            
        if event.type == MOUSEBUTTONUP:
            option1 = select_goku.check_click(x,y)
            option2 = select_vegeta.check_click(x,y)
            option3 = select_trunks.check_click(x,y)
            
    if player == None:
        if option1 != None or option2 != None or option3 != None:
            if option1 != None:
                player = option1
                print("player selected = %s"%(player.get_name()))
            if option2 != None:
                player = option2
                print("player selected = %s"%(player.get_name()))
            if option3 != None:
                player = option3
                print("player selected = %s"%(player.get_name()))
            player_added = True
            

    screen.blit(background, (0,0))

    
##    gx, gy =(goku.get_select_x(), goku.get_default_y()) 
##    rx, ry = (raditz.get_select_x(), raditz.get_default_y())
##    tx, ty = (trunks.get_select_x(), trunks.get_default_y())
    
    goku.update(ticks, 180,gx,gy, "", False)
    vegeta.update(ticks, 180,vx,vy, "", False)
    trunks.update(ticks, 180, tx, ty, "", False)
    select_group.update(x,y)
    select_group.draw(screen)
    character_group.draw(screen)
    pygame.display.update()

pygame.quit()
sys.exit()



