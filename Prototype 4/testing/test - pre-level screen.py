import pygame, sys, os
from characterV4 import *
from character_responce import *
from level_top_display import *

def display_text(screen, text, current_time):
    if (current_time // 1000) <= 3:
        screen.blit(text[0], (430, 220))
        return False
    elif 3 < (current_time // 1000) <= 6:
        screen.blit(text[1], (435,220))
        return False
    elif 6 < (current_time // 1000) <= 9:
        screen.blit(text[2], (430,220))
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((997,473))
pygame.display.set_caption("test - pre-level")

#player setup
player = Goku(screen)
group = pygame.sprite.Group()
group.add(player)
player._setx(100)
player._sety(player.get_default_y())
player.default()

#enemy setup
enemy = Raditz_enemy(screen)
enemy._setx(800)
enemy._sety(enemy.get_default_y())
enemy.set_bool_reversed(True)
enemy.default()
group.add(enemy)

#background setup
path1 = os.path.join("spritesheets", "backgrounds", "level1", "background.png")
path2 = os.path.join("spritesheets", "backgrounds", "level1", "background2.png")
backgrounds = (pygame.image.load(path1), pygame.image.load(path2))

#number setup
digit_1 = number(0)
digit_2 = number(1)
digit_3 = number(2)
number_group = pygame.sprite.Group()
number_group.add(digit_1)
number_group.add(digit_2)
number_group.add(digit_3)

#healthbar setup
player.set_health_bar(health_bar(player,screen,False))
enemy.set_health_bar(health_bar(enemy,screen,True))
healthbar_group = pygame.sprite.Group()
healthbar_group.add(player.get_health_bar())
healthbar_group.add(enemy.get_health_bar())

#text setup
stage_path = os.path.join("spritesheets", "pre_level", "stage1.png")
ready_path = os.path.join("spritesheets", "pre_level", "ready.png")
fight_path = os.path.join("spritesheets", "pre_level", "fight!.png")
text = (pygame.image.load(stage_path), pygame.image.load(ready_path), pygame.image.load(fight_path))


#level setup
framerate = pygame.time.Clock()
level_start = False
#don't need to setup player and enemy reaction

while not level_start:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    #-use dummy reaciton function
    if not player.get_animating():
        if player.get_default_mode():
            pass
        else:
            player.default()

    if not enemy.get_animating():
        if enemy.get_default_mode():
            pass
        else:
            enemy.default()


    screen.blit(backgrounds[0], (0,0))
    screen.blit(backgrounds[1],(0,267))
    player.update(ticks, 180, player._getx(), player._gety(), "", False)
    enemy.update(ticks, 180, enemy._getx(), enemy._gety(), "", False)
    healthbar_group.update()
    healthbar_group.draw(screen)
    number_group.update(300)
    number_group.draw(screen)
    group.draw(screen)

    level_start = display_text(screen, text, ticks)

    pygame.display.update()

if level_start:
    print("level begins")
    pygame.quit()
    sys.exit()

    
    

