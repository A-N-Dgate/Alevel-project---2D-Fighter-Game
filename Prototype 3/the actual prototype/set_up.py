import pygame, os
from character import *
from select_sprites import *
from level_top_display import *
from action_classes import *

#------------------all---------------------------
def setup_screen():
    pygame.init()
    screen = pygame.display.set_mode((997,473),0,32)
    pygame.display.set_caption("Prototype 3")
    return screen

def print_text(screen,  x, y, text,size, colour = (0,0,0)):
    font = pygame.font.Font(None, size)
    imgText = font.render(text, True, colour)
    screen.blit(imgText, (x,y))

def add_group(sprites):
    group = pygame.sprite.Group()
    for item in sprites:
        group.add(item)
    return group

#------------------levels------------------------
def load_level_background(level):

    path = os.path.join("spritesheets","backgrounds", "level%s" %(level), "background.png")
    background = pygame.image.load(path)

    path1 = os.path.join("spritesheets","backgrounds", "level%s" %(level), "background2.png")
    background2 = pygame.image.load(path1)

    return background, background2

def set_level_positions(screen,player, enemy):
    player.default()
    enemy.default()

    player._setx(100)
    enemy._setx(800)

    player._sety(player.get_default_y())
    enemy._sety(enemy.get_default_y())
    enemy.set_bool_reversed(True)

    player_healthbar = health_bar(player,screen,False)
    enemy_healthbar = health_bar(enemy,screen,True)
    player.set_health_bar(player_healthbar)
    enemy.set_health_bar(enemy_healthbar)

    return player_healthbar, enemy_healthbar


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

def set_move_enemy():
    punch = action_enemy("punch", False, False, "")
    block = action_enemy("block", False, False, "")
    chop = action_enemy("chop", False, False, "")
    kick = action_enemy("kick", False, False, "")
    jump = action_enemy("jump", True, True, "jump")
    crouch = action_enemy("crouch", True, False, "")
    right = action_enemy("right", True, True, "right")
    left = action_enemy("left", True, True, "left")
    down = action_enemy("down", True, True, "down")
    default = action_enemy("default", False, False, "")

    return punch,block,chop,kick,jump,crouch,right,left,down,default

def set_timer(ticks):
    time = ticks
    return time

def set_digits():
    digit_1 = number(0)
    digit_2 = number(1)
    digit_3 = number(2)

    return [digit_1, digit_2, digit_3]

def get_prelevel_images(level):
    #returns a tuple of images which are seperated in sprite interactions
    stage_path = os.path.join("spritesheets", "pre_level", "stage%s.png" %(level))
    ready_path = os.path.join("spritesheets", "pre_level", "ready.png")
    fight_path = os.path.join("spritesheets", "pre_level", "fight.png")

    stage = pygame.image.load(stage_path)
    ready = pygame.image.load( ready_path)
    fight = pygame.image.load(fight_path)

    return (stage, ready, fight)

def get_endlevel_images():
    lose_path = os.path.join("spritesheets", "end_level", "lose.png")
    win_path = os.path.join("spritesheets", "end_level", "win.png")
    time_path = os.path.join("spritesheets", "end_level", "time.png")

    lose = pygame.image.load(lose_path)
    win = pygame.image.load(win_path)
    time = pygame.image.load(time_path)

    return (lose,win,time)

#------------------character selection---------------

def character_select_positions(screen):
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

    goku_path = os.path.join("spritesheets", "select_sprites", "select_goku.png")
    trunks_path = os.path.join("spritesheets", "select_sprites", "select_trunks.png")
    vegeta_path = os.path.join("spritesheets", "select_sprites", "select_vegeta.png")
    
    select_goku = character_selection_sprite(screen, goku,goku_path, 25,110)
    select_vegeta= character_selection_sprite(screen, vegeta,vegeta_path, 350, 110)
    select_trunks = character_selection_sprite(screen, trunks,trunks_path, 675,110)

    characters = [goku, vegeta, trunks]
    select_sprites = [select_goku, select_vegeta, select_trunks]


    return (characters, select_sprites)


#------------------main menu---------------------------

def menu_setup(screen):
    arcade_path = os.path.join("spritesheets", "select_sprites", "arcade.png")
    exit_path = os.path.join("spritesheets", "select_sprites", "exit.png")
    practice_path = os.path.join("spritesheets", "select_sprites", "practice_mode.png")
    controls_path = os.path.join("spritesheets", "select_sprites", "controls.png")

    arcade_mode = menu_select_sprite(screen, arcade_path, 445, 220, 133,38)
    controls = menu_select_sprite(screen, controls_path, 412,330 , 183, 38)
    practice_mode = menu_select_sprite(screen, practice_path, 420, 277 , 171, 38)
    exit_select = menu_select_sprite(screen, exit_path, 465, 381,83, 38)

    return (arcade_mode, controls, practice_mode, exit_select)
    
