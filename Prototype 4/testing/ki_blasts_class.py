import pygame, os, sys, math
from characterV4 import *

class ki_blasts(pygame.sprite.Sprite):
    def __init__(self, attack, character):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0
        self.character = character
        self.attack_name = attack
        path = os.path.join("spritesheets","characters", self.character.get_name(), "%s.png" %(self.attack_name))
        self.master_image = pygame.image.load(path)
        self.image = None #set in the update method
        self.hitbox = None
        self.image_box = None
        #^if hitbox needs to be ammended, rect =/= hitbox
        self.group = pygame.sprite.Group()
        self.group.add(self)

    def _gety(self): return self.y
    def _sety(self, a): self.y = a

    def _getx(self): return self.x
    def _setx(self, a): self.x = a

    def get_hitbox(self): return self.hitbox
    def get_character(self): return self.character

    def check_attack(self, enemy):
        pass
    #^might not need this method


class kamehameha(ki_blasts):
    def __init__(self, character):
        ki_blasts.__init__(self, "kamehameha", character)
        self.frame = 0
        self.last_frame = 3
        self.rect = pygame.Rect(0,0,480,45)

        self.x = self.character._getx() + self.character.hitbox_width 
        self.y = self.character._gety() + 30

    def update(self, screen):
        if self.get_character().frame > 77:
        #^previous frames is getting the attack ready
            self._setx(self.character._getx() + self.character.hitbox_width)
            if not self.character.get_default_mode() and self.frame == 3:
                self.frame = 3
                if self.character.get_reversed():
                    self.hitbox = pygame.Rect((self.x - 70), self.y, -(120 * 4), 45)
                else:
                    self.hitbox = pygame.Rect(self.x, self.y, (120 * 4), 45)
            else:
                self.old_frame = self.frame - 1
                self.frame += 1
                if self.frame > self.last_frame:
                    self.kill()
                    self.get_character().set_blast(False)

            if self.frame != self.old_frame:
                frame_x = (self.frame % 4) * 480

                self.rect = pygame.Rect(frame_x, 0, 480,45)
                self.image = self.master_image.subsurface(self.rect)
                if self.character.get_reversed():
                    self.image = pygame.transform.flip(self.image, True, False)
                    self._setx(self._getx() - 550)
                self.hitbox = pygame.Rect(self.x, self.y, (120 * self.frame), 45)
                self.rect = self.hitbox
                self.old_frame = self.frame

            pygame.draw.rect(self.character.screen, (255,0,0), self.hitbox, 2)
            
            
            self.group.draw(screen)


class death_ball(ki_blasts):
    def __init__(self, character):
        ki_blasts.__init__(self, "death_ball", character)
        self.frame = 0
        self.old_frame = -1
        self.last_frame = 4
        self.rect = pygame.Rect(0,0,116,120)

        self.current_charframe = 0
        self.prev_charframe = 0
        self.angle = 90
        self.projectile = False
        self.draw = False
        self.rotation_angle = 0

        self.x = self.character._getx() - 25
        self.y = self.character._gety() - 150

    def update(self,screen):
        self.get_character().set_attack_power(50)
        self.set_projectile()
        self.set_draw()

        if 78 <= self.get_character().get_frame() <= 83:
            self.current_charframe += 1
            #let the ball grow in size...
            if self.frame >= self.last_frame:
                self.frame = 4
                #...if it hasn't reached full size
                
            if self.current_charframe == (self.prev_charframe + 3):
                #^ to add a delay in frame changes
                self.frame += 1
                self.prev_charframe = self.current_charframe
                    
        elif self.projectile:
            #ball moves with projectile motion
            self.frame = 4
                
            self.angle = (self.angle - 1) % 360
            dx = math.sin(math.radians(self.angle)) * 15
            dy = math.cos(math.radians(self.angle)) * 15

            if self.get_character().get_reversed():
                dx = -dx
                
            self.rotation_angle = (-math.degrees(math.atan2(dy,dx))) % 360

            self._setx(self._getx() + dx)
            self._sety(self._gety() + dy)
                    
                

        self.old_frame = self.frame - 1
        if self.frame != self.old_frame:
            frame_x = (self.frame % 5) * 116
            self.rect = pygame.Rect(frame_x, 0, 116, 120)
            self.image = self.master_image.subsurface(self.rect)
            self.image_box = pygame.Rect(self.x, self.y, 116, 120)
            self.rect = self.image_box
            self.hitbox = pygame.Rect((self.x + 29), (self.y + 30), 58, 60)
            self.old_frame = self.frame

            if self.projectile:
                self.image = pygame.transform.rotate(self.image, self.rotation_angle)

            if self._gety() > 473 or self.get_character().get_blast_hit():
                #print("y vlaue: %d, blast hit: %s" %(self._gety(), self.get_character().get_blast_hit()))
                self.kill()
                self.get_character().set_blast(False)
            else:
                self.get_character().set_blast(True)
                if self.get_character().get_frame() >= 85:
                    self.get_character().set_frame(85)
            
        if self.draw:
            self.group.draw(screen)
            pygame.draw.rect(self.character.screen, (255,0,0), self.hitbox, 2)

            

    def set_projectile(self):
        if not self.projectile and self.get_character().get_frame() >= 83:
            self.projectile = True

    def set_draw(self):
        if self.get_character().frame >= 78:
            self.draw = True

            
                

    


            
            
        
        
        
