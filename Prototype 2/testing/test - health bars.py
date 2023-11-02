import pygame, sys
from characterV2 import *


class health_bar():
    def __init__(self, character, target, enemy):
        self.character = character
        self.screen = target
        self.enemy = enemy
        self.added_x = 0
        self.image = None #added in a later prototype
        self.starting_width = 400
        self.width = 400
        self.height = 20
        if self.enemy:
            self.bar_x = self.x = 575 
        else:
            self.bar_x = self.x = 10 
        self.y = 10 
        self.bar_rect = pygame.Rect(self.bar_x,self.y,self.width,self.height)
        self.health_rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.colour = (0,255,0)
        #green --> orange --> red

    def get_health_rect(self): return self.health_rect
    def get_bar_rect(self): return self.bar_rect
    
    def set_rectangles(self): 
        self.bar_rect = pygame.Rect(self.bar_x,self.y,self.starting_width,self.height)
        self.health_rect = pygame.Rect((self.x+self.added_x),self.y,self.width,self.height)

    def character_hit(self):
        #changes the length, position and the colour of the health bar
        value = self.character.get_health()
        total = self.character.get_original_health()
        percentage_left = value / total
        self.width = int(self.starting_width * percentage_left)

        if self.enemy:
            percentage_taken = 1 - percentage_left
            self.added_x = (self.starting_width * percentage_taken) 

        if 0.25 < percentage_left <= 0.5 and self.colour != (255,160,0):
            self.colour = (255,160,0)

        elif percentage_left <= 0.25 and self.colour != (255,0,0):
            self.colour = (255,0,0)

        self.set_rectangles()

    def update(self):
        #self.screen.blit(self.image(self.bar_x,self.y))
        pygame.draw.rect(self.screen, (0,0,0), self.bar_rect, 0)
        pygame.draw.rect(self.screen, self.colour, self.health_rect, 0)

    def remove_health_rect(self):
        self.health_rect = pygame.Rect(0,0,0,0)


pygame.init()
screen = pygame.display.set_mode((997,453))
framerate = pygame.time.Clock()
player = Goku(screen)
enemy = Raditz(screen)
group = pygame.sprite.Group()
group.add(player)
group.add(enemy)
goku_health_bar = health_bar(player,screen,False)
raditz_health_bar = health_bar(enemy,screen,True)

player._setx(0)
player._sety(player.values[0])
player.default()

enemy._setx(800)
enemy._sety(enemy.values[0])
enemy.default()

while True:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        user_input = pygame.key.get_pressed()
        
        if user_input[K_a]:
            player.set_health(player.get_health() - 5)
            player.set_dead()
            player.hit()
            goku_health_bar.character_hit()

        if user_input[K_l]:
            enemy.set_health(enemy.get_health() - 5)
            enemy.set_dead()
            enemy.hit()
            raditz_health_bar.character_hit()

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
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


    screen.fill((255,255,255))

    if not player.get_dead() or not enemy.get_dead():
        player.set_reversed(enemy)
        player.update(ticks, 180, player._getx(), player._gety(), "")
        goku_health_bar.update()
        enemy.set_reversed(player)
        enemy.update(ticks,180,enemy._getx(), enemy._gety(), "")
        raditz_health_bar.update()
        
    if player.get_dead() or enemy.get_dead():
        if player.get_dead():
            player.defeated()
            player.set_reversed(enemy)
            player.update(ticks, 180, player._getx(), player._gety(), "")
            goku_health_bar.remove_health_rect()
            goku_health_bar.update()
            enemy.set_reversed(player)
            enemy.update(ticks,180,enemy._getx(), enemy._gety(), "")
            raditz_health_bar.update()
        elif enemy.get_dead():
            enemy.defeated()
            enemy.set_reversed(player)
            enemy.update(ticks, 180, player._getx(), player._gety(), "")
            raditz_health_bar.remove_health_rect()
            raditz_health_bar.update()
            player.set_reversed(enemy)
            player.update(ticks,180,enemy._getx(), enemy._gety(), "")
            goku_health_bar.update()

    group.draw(screen)
    pygame.display.update()
    
    
            
        
        
        
        
