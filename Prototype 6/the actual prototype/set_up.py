import pygame, os
from character import *
from select_sprites import *
from level_top_display import *
from character_extras import *

#------------------all---------------------------
def setup_screen():
    pygame.init()
    screen = pygame.display.set_mode((997,473),0,32)
    pygame.display.set_caption("Prototype 5")
    return screen

def print_text(screen,  x, y, text,size, colour = (255,255,255)):
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

    path = os.path.join("spritesheets","backgrounds", "level%d" %(level), "background.png")
    background = pygame.image.load(path)

    path1 = os.path.join("spritesheets","backgrounds", "level%d" %(level), "background2.png")
    background2 = pygame.image.load(path1)

    return background, background2

def play_level_music(level):
    pygame.mixer.music.load(os.path.join("sfx", "level%d.mp3"%(level)))
    pygame.mixer.music.play(-1)

def set_level_positions(screen, player, enemy):
    player.default()
    enemy.default()

    player._setx(100)
    enemy._setx(800)

    player.set_health(player.get_original_health())

    player._sety(player.get_default_y())
    enemy._sety(enemy.get_default_y())
    enemy.set_bool_reversed(True)

    enemy.set_health_bar(health_bar(enemy,screen,True))
    player.set_health_bar(health_bar(player,screen,False))


def level_values():
    #in order of the original level1 function
    return pygame.time.Clock(), [], set_move(), set_move_enemy(),True, False, True, [False,False,False,False],pygame.time.get_ticks()

def set_enemy(screen,level):
    enemies = [Raditz_enemy(screen), Frieza_enemy(screen), Cell_enemy(screen)]
    for enemy in enemies:
        if enemy.get_level() == level:
            return enemy
           

def level_setup(screen,player,level):
    screen.fill((255,255,255))
    backgrounds = load_level_background(level)
    enemy = set_enemy(screen,level)

    timer_numbers = set_digits()

    return enemy,timer_numbers
    
    


def set_move():
    punch = action("punch", False, False, "")
    block = action("block", False, False, "")
    chop = action("chop", False, False, "")
    kick = action("kick", False, False, "")
    jump = action("jump", True, True, "jump")
    crouch = action("crouch", True, False, "")
    right = action("move_right", True, True, "right")
    left = action("move_left", True, True, "left")
    down = action("back_down", True, True, "down")
    default = action("default", False, False, "")

    return (punch, block, chop, kick, jump, crouch, right, left, down, default)

def set_move_enemy():
    punch = action_enemy("punch", False, False, "")
    block = action_enemy("block", False, False, "")
    chop = action_enemy("chop", False, False, "")
    kick = action_enemy("kick", False, False, "")
    jump = action_enemy("jump", True, True, "jump")
    crouch = action_enemy("crouch", True, False, "")
    right = action_enemy("move_right", True, True, "right")
    left = action_enemy("move_left", True, True, "left")
    down = action_enemy("back_down", True, True, "down")
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
    stage_path = os.path.join("spritesheets", "pre_level", "stage%d.png" %(level))
    ready_path = os.path.join("spritesheets", "pre_level", "ready.png")
    fight_path = os.path.join("spritesheets", "pre_level", "fight!.png")

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

    #extra button to switch between screens
    extra_path = os.path.join("spritesheets", "select_sprites", "extra.png")
    extra_button = menu_select_sprite(screen, extra_path, 450, 60, 116,38)


    return ([goku, vegeta, trunks], [select_goku, select_vegeta, select_trunks, extra_button])


def extra_characters_positions(screen,player_data):
    raditz = Raditz(screen)
    frieza = Frieza(screen)
    cell = Cell(screen)

    raditz.default()
    frieza.default()
    cell.default()

    raditz._setpos((raditz.get_select_x(),raditz.get_default_y()))
    frieza._setpos((frieza.get_select_x(),frieza.get_default_y()))
    cell._setpos((cell.get_select_x(),cell.get_default_y()))

    raditz_path = os.path.join("spritesheets", "select_sprites", "select_raditz.png")
    frieza_path = os.path.join("spritesheets", "select_sprites", "select_frieza.png")
    cell_path = os.path.join("spritesheets", "select_sprites", "select_cell.png")

    select_raditz = unlockable_character_select_sprite(screen, raditz, raditz_path, 25, 110, player_data.select_raditz())
    select_frieza = unlockable_character_select_sprite(screen, frieza, frieza_path, 350,110, player_data.select_frieza())
    select_cell = unlockable_character_select_sprite(screen, cell, cell_path, 675,110, player_data.select_cell())

    #back button to go back to original character screen
    back_path = os.path.join("spritesheets","select_sprites", "back.png")
    back_button = menu_select_sprite(screen, back_path, 460,60, 91,38)

    return ([raditz,frieza,cell],[select_raditz,select_frieza,select_cell,back_button])

def get_character_select_values():
    return False, None, 0, 0
    
def play_char_select_music():
    #because of recursive algorithm, this has to be called in main code
    pygame.mixer.music.load(os.path.join("sfx", "char_select.mp3"))
    pygame.mixer.music.play(-1)

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

def play_menu_music():
    pygame.mixer.music.load(os.path.join("sfx", "main_menu.mp3"))
    pygame.mixer.music.play(-1)


#------------------practice mode---------------------------

def practicemode_game_setup():
    #in order: moves, action_queue, keydown, framerate, previous_list, exit_game, mouse_x, mouse_y
    moves = set_move()
    framerate = pygame.time.Clock()
    return moves, [],[False, False, False, False], framerate, [], False, 0 ,0

def exitbutton_setup(screen):
    exit_path = os.path.join("spritesheets", "select_sprites", "exit.png")
    exit_select = menu_select_sprite(screen, exit_path, 455, 10, 83, 38)

    group = pygame.sprite.Group()
    group.add(exit_select)
    
    return exit_select, group


#------------------end level screen---------------------------

def setup_enemy_icons(screen,current_level,win):
    
    level1 = Raditz_enemy(screen)
    level2 = Frieza_enemy(screen)
    level3 = Cell_enemy(screen)
    
    level1.get_icon().set_image_enemy(current_level,win)
    level2.get_icon().set_image_enemy(current_level,win)
    level3.get_icon().set_image_enemy(current_level,win)

    level1.get_icon()._setpos((500,300))
    level2.get_icon()._setpos((500,200))
    level3.get_icon()._setpos((500,100))

    #because the enemy icons don't update:
    level1.get_icon().set_rect_enemy()
    level2.get_icon().set_rect_enemy()
    level3.get_icon().set_rect_enemy()

    return level1,level2,level3

def setup_player_icon(player,win, current_enemy):
    player.get_icon().set_outcome(win)
    player.get_icon().set_image()
    player.get_icon()._setpos((400, current_enemy.get_icon()._gety()))
    


def get_current_enemy(enemies, current_level):
    for enemy in enemies:
        if enemy.get_level() == current_level:
            return enemy

def get_next_enemy(enemies, current_level):
    for enemy in enemies:
        try:
            if enemy.get_level() == current_level + 1:
                return enemy
        except: #end of enemy tree
            return None

def endlevel_values():
    return pygame.time.Clock(), False

def play_endlevel_music():
    pygame.mixer.music.load(os.path.join("sfx", "end_level.mp3"))
    pygame.mixer.music.play(-1)


#-----------------------------controls screen-----------------------------

def controls_screen_setup(screen):
    control_background = pygame.image.load(os.path.join("spritesheets", "backgrounds", "controls_screen.png"))
    back_button = os.path.join("spritesheets", "select_sprites", "back.png")

    backbutton = menu_select_sprite(screen, back_button,450,410,91,38)
    return control_background, backbutton, False, pygame.time.Clock()


#-------------------------loading data ----------------------------------

def start_arcade_setup(screen):
    ld_path = os.path.join("spritesheets", "select_sprites", "load_data.png")
    ng_path = os.path.join("spritesheets", "select_sprites", "new_game.png")

    load_data = menu_select_sprite(screen, ld_path, 350, 250, 292,38)
    new_game = menu_select_sprite(screen, ng_path, 405, 315, 172,38)

    return load_data, new_game


def start_practice_setup(screen):
    ld_path = os.path.join("spritesheets", "select_sprites", "load_data.png")
    dld_path = os.path.join("spritesheets", "select_sprites", "dont_load.png")

    load_data = menu_select_sprite(screen,ld_path, 350, 250, 292,38)
    dont_load = menu_select_sprite(screen,dld_path, 345,315,303,38)

    return load_data, dont_load 

def get_load_data_values():
    return False, False, False, pygame.time.Clock()

def get_enter_name_values():
    return False, [], pygame.time.Clock()

def enter_name_setup():
    text_rect = pygame.image.load(os.path.join("spritesheets", "start_arcade", "text_rect.png")) .convert()
    #.convert_alpha converts the image so that pixels can be maipulated
    text_rect.set_alpha(150)
    #makes the rect translucent, where 150 is the value of transparency
    enter_name = pygame.image.load(os.path.join("spritesheets", "start_arcade", "name.png"))

    return text_rect, enter_name
    



    
