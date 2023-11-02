import pygame,os,sys
from select_sprites import *
from pygame.locals import *

def print_text(screen,  x, y, text,size, colour = (255,255,255)):
    font = pygame.font.Font(None, size)
    imgText = font.render(text, True, colour)
    screen.blit(imgText, (x,y))
    
#all code here for the start_arcade main function (might slpit into two)
#seperate into functions/procedures in P5 with using the data methods

pygame.init()
screen = pygame.display.set_mode((997,473))
pygame.display.set_caption("Test - Loading data GUI")

#start arcade set up
background = pygame.image.load(os.path.join("spritesheets", "backgrounds", "menu_background.png"))
ld_path = os.path.join("spritesheets", "select_sprites", "load_data.png")
ng_path = os.path.join("spritesheets", "select_sprites", "new_game.png")
x = 350
y = 250


load_data = menu_select_sprite(screen, ld_path, x, y,292,38)
new_game = menu_select_sprite(screen, ng_path, (x+55), (y+65),172,38)
group = pygame.sprite.Group()
group.add(load_data)
group.add(new_game)

select = False
option1 = False
option2 = False
framerate = pygame.time.Clock()
x = y = 0

#sprite interactions start - use select_eventcheck function and then create
# a check click function
while not select: #while true; return statement breaks the loop
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEMOTION:
            x,y = pygame.mouse.get_pos()

        if event.type == MOUSEBUTTONUP:
            option1 = load_data.check_click(x,y)
            option2 = new_game.check_click(x,y)

    if option1 or option2:
        if option1:
            load = True
            print("load data")
            select = True
        elif option2:
            new = True
            print("new game")
            select = True
        #^these would be return statements as tuples with both booleans


    #update
    group.update(x,y)
    screen.blit(background, (0,0))
    group.draw(screen)

    pygame.display.update()

#load data and new game functions; they share entering player name
enter = False
letters = []


text_rect = pygame.image.load(os.path.join("spritesheets", "start_arcade", "text_rect.png")) .convert()
text_rect.set_alpha(150)
enter_name = pygame.image.load(os.path.join("spritesheets", "start_arcade", "name.png"))



while not enter:
    player_name = ""
    #^reset so that removed letters can be removed from the string
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    #create enter name event check
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == KEYDOWN:
            if event.key == pygame.K_RETURN:
                enter = True
                
            elif len(pygame.key.name(event.key)) > 1:
                #check backspce
                if event.key == pygame.K_BACKSPACE:
                    try:
                        letters.pop()
                    except IndexError:
                        pass
                    
            else:
                letters.append(pygame.key.name(event.key))


    for letter in letters:
        if len(player_name) >= 1:
            if letter not in player_name:
                player_name += letter
        else:
            player_name += letter

    
    #update
    screen.blit(background,(0,0))
    screen.blit(text_rect,(270,320))
    screen.blit(enter_name, (355,255))
    print_text(screen, 270, 320,player_name.upper(),100)

    pygame.display.update()


print("player name = %s" %(player_name))
    
    



pygame.quit()
sys.exit()
