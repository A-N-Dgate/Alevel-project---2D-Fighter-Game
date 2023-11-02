import pygame, os
from character import *

#------------------all---------------------------
def setup_screen():
    pygame.init()
    screen = pygame.display.set_mode((997,473),0,32)
    pygame.display.set_caption("Prototype 2")
    return screen

def print_text(screen,  x, y, text,size, colour = (0,0,0)):
    font = pygame.font.Font(None, size)
    imgText = font.render(text, True, colour)
    screen.blit(imgText, (x,y))

def add_group(characters):
    #characters = list of the characters on screen
    group = pygame.sprite.Group()
    for item in characters:
        group.add(item)
    return group

#------------------levels------------------------
def load_level_background(level):
    path = os.path.join("spritesheets", "level1", "background.png") #%(level))
    background = pygame.image.load(path)

    path1 = os.path.join("spritesheets", "level1", "background2.png") #%(level))
    background2 = pygame.image.load(path1)

    return background, background2

def set_level_positions(screen,player, enemy):
    player.default()
    enemy.default()

    player._setx(100)
    enemy._setx(800)

    player._sety(player.get_default_y())
    enemy._sety(enemy.get_default_y())

    player_healthbar = health_bar(player,screen,False)
    enemy_healthbar = health_bar(enemy,screen,True)
    player.set_health_bar(player_healthbar)
    enemy.set_health_bar(enemy_healthbar)

    return player_healthbar, enemy_healthbar
    

#------------------character selection---------------

def character_select_positions(screen):
    goku = Goku(screen)
    raditz = Raditz(screen)
    trunks = Trunks(screen)

    goku.default()
    raditz.default()
    trunks.default()

    gx, gy =(goku.get_select_x(), goku.get_default_y()) 
    rx, ry = (raditz.get_select_x(), raditz.get_default_y())
    tx, ty = (trunks.get_select_x(), trunks.get_default_y())

    goku._setpos((gx, gy))
    raditz._setpos((rx, ry))
    trunks._setpos((tx, ty))

    image_path = os.path.join("spritesheets", "select_sprites", "select_sprite.png")
    #^change image within class when sprite is made
    select_goku = selection_sprite(screen, goku,image_path, 25,110,2)
    select_raditz = selection_sprite(screen, raditz,image_path, 350, 110,1)
    select_trunks = selection_sprite(screen, trunks,image_path, 675,110,0)

    characters = [goku, raditz, trunks]
    select_sprites = [select_goku, select_raditz, select_trunks]


    return (characters, select_sprites)
