import pygame, sys, os, time
from animating_sprites import *

class character(my_sprite):
    def __init__(self,name, target):
        my_sprite.__init__(self, target)
        self.name = name.title()
        self.health = 0
        self.attack_power = 0
        self.defence = 0
        self.hitbox_height = 0
        self.hitbox_width = 0
        self.hitbox = pygame.Rect(0,0, self.hitbox_width, self.hitbox_height)
        self.animating = False
        self.default_mode = True
        self.blocking = False
        self.attacking = False
        self.reversed = False
        self.dead = False
        self.being_attacked = False

    #set the health, attack power and defence according to which character is selected
    def get_health(self): return self.health
    def set_health(self, health): self.health = health

    def get_attack_power(self): return self.attack_power
    def set_attack_power(self, power): self.attack_power = power

    def get_defence(self): return self.defence
    def set_defence(self, defence): self.defence = defence

    def get_animating(self): return self.animating
    def set_animating(self, a): self.animating = a

    def get_default_mode(self): return self.default_mode
    def set_default_mode(self, a): self.default_mode = a

    def get_attacking(self): return self.attacking
    def set_attacking(self, a): self.attacking = a

    def get_attacked(self): return self.being_attacked
    def set_attacked(self, a): self.being_attacked = a

    def get_reversed(self): return self.reversed
    def set_reversed(self, oposition): #character object
        if self._getx() >= oposition._getx():
            self.reversed = True
        else:
            self.reversed = False

    def get_dead(self): return self.dead
    def set_dead(self):
        if self.health < 0:
            self.dead = True
        else:
            self.dead = False

    #making sure that when the frame is updated, the hit box is updated as well
    def get_hitbox(self): return self.hitbox
    def set_hitbox(self, x, y):
        path = os.path.join("spritesheets", str(self.name), "dimensions.txt")
        file = open(path, "r")
        for line in file:
            line = line.split(",")
            if int(line[0]) == self.frame:
                self.hitbox_width = int(line[1]) + 10
                self.hitbox_height = int(line[2].rstrip()) + 10

        file.close()
        
        if self.reversed:
            x += self.hitbox_width // 2
            
        self.hitbox = pygame.Rect(x, (y+ (self.hitbox_height // 4)), self.hitbox_width, self.hitbox_height)

    def update(self,current_time, rate, x, y, mode): #x and y resets the movement
        #update the animation frame number
        self.old_frame = self.frame - 1
        if current_time > self.last_time + rate: 
            self.frame += 1
            if self.frame >= self.last_frame:
                if self.animating:
                    self.animating = False
                else:
                    #default and defeated animations:
                    if self.frame > self.last_frame:
                        self.frame = self.first_frame
            self.last_time = current_time

        #build on current frame only if it changed
        if self.frame != self.old_frame: 
            #gets current frame by covering up master image
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            self.rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(self.rect)
            self.rect = self.hitbox
            self.old_frame = self.frame

            if self.reversed:
                self.image = pygame.transform.flip(self.image, True, False)

            if mode != "":
                pos = self.movement(mode, x, y)
                x = pos[0]
                y = pos[1]

            else:
               self._setx(x)
               self._sety(y)

            self.set_hitbox(x, y)

    def move(self, dx, dy, x, y):
        self._setx(x + dx)
        self._sety(y + dy)
        return (self._getx(), self._gety())
        #and the hitbox will be updated in the update() method

    def movement(self, mode, x, y):
        #making sure the character moves gradually when animating
        if mode == "right":
            return self.move(7.5,0, x, y) #5

        if mode == "left":
            return self.move(-7.5,0, x, y) #5

        if mode == "jump":
            return self.move(0, -3, x, y) #2

        if mode == "down":
            return self.move(0, 4.18, x, y) #3.5 

            
#setting the first and last frames for each action usng the spritesheet notes
#the frist frames don't show on screen so ive set the frist frame to the previous last frame
    def default(self):
        self.frame = 0
        self.last_frame = 3
        self.default_mode = True
        #reset atributes
        self.first_frame = 0
        self.blocking = False
        self.attacking = False
        self.being_attacked = False
        
    def crouch(self):
        self.frame = 3
        self.last_frame = 6
        self.animating = True
        self.default_mode = False

    def block(self):
        self.frame = 6
        self.last_frame = 10
        self.animating = True
        self.default_mode = False
        self.blocking = True

    def move_right(self):
        self.frame = 10 
        self.last_frame = 14
        self.animating = True
        self.default_mode = False

    def move_left(self):
        self.frame = 14
        self.last_frame = 17
        self.animating = True
        self.default_mode = False

    def jump(self):
        self.frame = 17
        self.last_frame = 22
        self.animating = True
        self.default_mode = False

    def back_down(self):
        self.frame = 22
        self.last_frame = 25
        self.animating = True
        self.default_mode = False

    def punch(self):
        self.frame = 25
        self.last_frame = 31
        self.animating = True
        self.default_mode = False
        self.attacking = True

    def kick(self):
        self.frame = 31
        self.last_frame = 36
        self.animating = True
        self.default_mode = False
        self.attacking = True

    def chop(self):
        self.frame = 37
        self.last_frame = 42
        self.animating = True
        self.default_mode = False
        self.attacking = True

    def low_punch(self):
        self.frame = 42
        self.last_frame = 47
        self.animating = True
        self.default_mode = False
        self.attacking = True

    def low_kick(self):
        self.frame = 47
        self.last_frame = 53
        self.animating = True
        self.default_mode = False
        self.attacking = True

    def low_block(self):
        self.frame = 53
        self.last_frame = 55
        self.animating = True
        self.default_mode = False

    def uppercut(self):
        self.frame = 55
        self.last_frame = 61
        self.animating = True
        self.default_mode = False
        self.attacking = True

    def high_kick(self):
        self.frame = 61 
        self.last_frame = 68
        self.animating = True
        self.default_mode = False
        self.attacking = True

    def hit(self):
        self.frame = 68
        self.last_frame = 72
        self.animating = True
        self.default_mode = False
        self.being_attacked = True

    def defeated(self):
        self.frame = 73
        self.first_frame = 73
        self.last_frame = 74
        self.animating = False
        self.default_mode = False

    def __str__(self):
    #edited the string method to show the hitbox instead of rect
        return str(self.frame) + "," + str(self.first_frame) + \
                "," + str(self.last_frame) + "," + str(self.frame_width) + \
                "," + str(self.frame_height) + "," + str(self.columns) + \
                "," + str(self.hitbox)

        
