import pygame, os, sys
from characterV2 import *


class selection_sprite(pygame.sprite.Sprite):
    def __init__(self, screen, character, image_path, x, y,):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.character = character
        self.width = 300
        self.height = 453
        self.rect = pygame.Rect(x,y,self.width, self.height)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.character_position = ((self.rect.x // 2),(self.rect.y + self.height))
        
    def check_click(self, mouse_x, mouse_y):
        if self.x < mouse_x < (self.x + 300):
            return self.character

    def get_character_position(self): return self.character_position
        
##    def animate_character(self, ticks):
##        self.character.update(ticks, 180, self.character_position[0], self.character_position[1], "")
        
        

pygame.init()
screen = pygame.display.set_mode((997,473))
pygame.display.set_caption("character select")
framerate = pygame.time.Clock()

goku = Goku(screen)
raditz = Raditz(screen)
goku2 = Goku(screen)

goku.default()
raditz.default()
goku2.default()

character_group = pygame.sprite.Group()
character_group.add(goku)
character_group.add(raditz)
character_group.add(goku2)
#for animating the characters 

image_path = os.path.join("spritesheets", "select_sprites", "test_image3.png")
select_goku = selection_sprite(screen, goku,image_path, 25,110)
select_raditz = selection_sprite(screen, raditz,image_path, 350, 110)
select_goku2 = selection_sprite(screen, goku2,image_path, 675,110)

select_group = pygame.sprite.Group()
select_group.add(select_goku)
select_group.add(select_raditz)
select_group.add(select_goku2)
# cant do group.check_click()

##goku._setpos(select_goku.get_character_position())
##raditz._setpos(select_raditz.get_character_position())
##print(select_goku.get_character_position())
gx, gy =(130, 320) 
rx, ry = (440, 305)
g2x,g2y = (780, 320)


goku._setpos((gx, gy))
raditz._setpos((rx, ry))
goku2._setpos((g2x,g2y))


player = None
option1 = None
option2 = None
option3 = None

player_added = False
x = y = 0

while not player_added:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == MOUSEBUTTONUP:
            x,y = pygame.mouse.get_pos()
            
    if player == None:
        option1 = select_goku.check_click(x,y)
        option2 = select_raditz.check_click(x,y)
        option3 = select_goku2.check_click(x,y)
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
            

    screen.fill((255,255,255))
##    select_goku.animate_character(ticks)
##    select_raditz.animate_character(ticks)
##    goku.transform_image(2,2)
##    raditz.transform_image(2,2)
##    #add later within class update method
    goku.update(ticks, 180,gx,gy, "")
    raditz.update(ticks, 180,rx,ry, "")
    goku2.update(ticks, 180, g2x, g2y, "")
    select_group.draw(screen)
    character_group.draw(screen)
    pygame.display.update()

#-----------------------------------------------------------
    #^function: character select loop and return player
    #dont know how much code to include in the function

pygame.quit()
sys.exit()

    

