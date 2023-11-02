#put with action classes and special move classes in prototype
import pygame,sys,os
from characterV4 import *

class icon(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.outcome = None
        self.x = 0
        self.y = 0
        self.width = 60
        self.height = 60
        self.frame = 0
        self.last_time = 0
        self.rect = pygame.Rect(0,0,0,0)
        self.master_image = pygame.image.load(os.path.join("spritesheets", "characters", "%s" %(name), "icon.png"))
        self.image = None

    def _getx(self): return self.x
    def _setx(self, a): self.x = a

    def _gety(self): return self.y
    def _sety(self, a): self.y = a

    def _getpos(self): return self.x,self.y
    def _setpos(self, a):
        #a --> tuple or list
        self._setx(a[0])
        self._sety(a[1])

    def get_outcome(self): return self.outcome
    def set_outcome(self, a): self.outcome = a

    def set_image(self):
        if self.outcome or self.outcome == None:
            self.frame = 0
        else:
            self.frame = 1

        self.rect = pygame.Rect((self.width * self.frame),0,self.width,self.height)
        self.image = self.master_image.subsurface(self.rect)  

    def update(self, current_time, rate, next_enemy):
        if self.outcome:
            if current_time > self.last_time + rate:
                self.y -= 5
                self.last_time = current_time
                self.rect = pygame.Rect(self.x ,self.y,self.width,self.height)
                if self.y == next_enemy.get_icon()._gety():
                    return True
            return False

        elif not self.outcome:
            if current_time > self.last_time + rate:
                self.y += 5
                self.last_time = current_time
                self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
                if self.y >= 473:
                    return True
            return False

    def set_rect_enemy(self): self.rect = pygame.Rect((self.x + (self.width * self.frame)),self.y,self.width,self.height)
        
            
                
            
