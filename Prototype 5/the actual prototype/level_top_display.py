import pygame, os

class number(pygame.sprite.Sprite):
    def __init__(self, digit):
        pygame.sprite.Sprite.__init__(self)
        self.number_displayed = 0
        self.digit = digit #0, 1 or 2 so that x coordinate can be changed
        self.x_value = 470
        self.x = 0
        self.y = 10
        self.rect = None
        self.image = None


    def update(self, time_remaining):
        time_remaining = str(time_remaining)
        self.number_displayed = time_remaining[self.digit]
        self.x = self.x_value + (14 * self.digit)
        self.rect = pygame.Rect(self.x, self.y, 14, 25)
        self.path = os.path.join("spritesheets", "numbers", "%s.png" %(self.number_displayed))
        self.image = pygame.image.load(self.path).convert_alpha()

    def get_x_value(self): return self.x_value
    def set_x_value(self, a): self.x_value = a

    def get_digit(self): return self.digit
    def set_digit(self, a): self.digit = a
    

class health_bar(pygame.sprite.Sprite):
    def __init__(self, character, target, enemy):
        self.character = character
        self.screen = target
        self.enemy = enemy
        self.added_x = 0 
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

        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(self.x, self.y, 400,20)
        if self.enemy:
            self.path = os.path.join("spritesheets", "health_bars", "enemy.png")
        else:
            self.path = os.path.join("spritesheets", "health_bars", "player.png")

        self.image = pygame.image.load(self.path)
            
        

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

        if percentage_left > 0.5 and self.colour != (0,255,0):
            self.colour = (0,255,0)

        if 0.25 < percentage_left <= 0.5 and self.colour != (255,160,0):
            self.colour = (255,160,0)

        elif percentage_left <= 0.25 and self.colour != (255,0,0):
            self.colour = (255,0,0)

        self.set_rectangles()

    def update(self):
        pygame.draw.rect(self.screen, (0,0,0), self.bar_rect, 0)
        pygame.draw.rect(self.screen, self.colour, self.health_rect, 0)

    def remove_health_rect(self):
        self.health_rect = pygame.Rect(0,0,0,0)

