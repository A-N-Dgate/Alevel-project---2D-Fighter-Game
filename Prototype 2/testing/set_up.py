import pygame, os
from character import *

def setup_screen():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Testing")
    return screen

def load_background(name):
    path = os.path.join("spritesheets", "Background1", name)
    background = pygame.image.load(path)
    return background
 
def set_positions(player, enemy):
    #player to enemy height difference = 15 at default
    
    player._setx(300)
    player._sety(295) 
    player.set_health(100)
    player.set_attack_power(5)
    player.default()

    enemy._setx(600)
    enemy._sety(275)
    enemy.set_health(100)
    enemy.set_attack_power(5)
    enemy.default()

def load_character(name, screen):
    character1 = character(name, screen)
    filename = "%sSheet.png" %(name)
    path = os.path.join("spritesheets", name, filename)
    dimentions = get_dimentions(name)
    width = int(dimentions[0])
    height = int(dimentions[1])
    character1.load(path, width, height, 75)
    return character1
    
def get_dimentions(name):
    #like the get_hitbox() method
    path = os.path.join("spritesheets", name, "dimensions.txt")
    file = open(path, "r")
    for line in file:
        line = line.split(",")
        if int(line[0]) == 75:
            dimentions = (line[1], line[2])
            #^ width, height
    return dimentions

def add_group(characters):
    #characters = list of the characters on screen
    group = pygame.sprite.Group()
    for item in characters:
        group.add(item)
    return group

def print_text(screen,  x, y, text,size, colour = (0,0,0)):
    font = pygame.font.Font(None, size)
    imgText = font.render(text, True, colour)
    screen.blit(imgText, (x,y))

