import pygame, sys, os, time
from animating_sprites import *

#-------hitboxes dont work; it did work in P1-------

class character(my_sprite):
    def __init__(self, name, target):
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
        #------added for P2------
        self.screen = target
        self.values = []
        self.attack_boxes = []
        self.attack_box = None
        #both values and attack boxes are set in the character subclasses
        self.in_air = False
        self.low = False
        self.high_attack = False
        #^to fix the original hitboxes
        self.attack_box_row = -1
        self.frame_number = 0 #frame number in the current animation cycle

    def get_rect(self): return self.rect

    def get_original_health(self): return self.original_health

    def get_health(self): return self.health
    def set_health(self, health): self.health = health

    def get_attack_power(self): return self.attack_power
    def set_attack_power(self, power): self.attack_power = power

    def get_defence(self): return self.defence
    def set_defence(self, defence): self.defence = defence

    def get_name(self): return self.name
    def set_name(self, name): self.name = name

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

        if self.in_air:
            self.hitbox_height -= self.hitbox_height * 0.2

        if self.low:
            y += self.default_height // 2
            self.hitbox_height -= self.hitbox_height * 0.2

        if self.high_attack:
            y -= self.hitbox_height * 0.2
                
        self.hitbox = pygame.Rect(x,(y+(self.hitbox_height // 4)) , self.hitbox_width, self.hitbox_height)
        
        #print(str(self.hitbox))
        
        if self.attacking:
            self.set_attack_box(x,y)
        #^ set the hitbox as the rect first

    def get_attack_box(self): return self.attack_box
    def set_attack_box(self, x, y):
        self.set_box_lists(x, y)
        #^ this should move to improve efficiency - move to move method
        box_list = self.attack_boxes[self.attack_box_row]
        current_box = box_list[self.frame_number]
        #print(current_box)

        if current_box != None:
            pass
            #self.rect = current_box
            #^ fix that later

            #pygame.draw.rect(self.screen, (0,0,255), current_box, 2)
            
       
        
    def update(self,current_time, rate, x, y, mode): #x and y resets the movement
        #update the animation frame number
        self.old_frame = self.frame - 1
        if current_time > self.last_time + rate: 
            self.frame += 1
            self.frame_number += 1
            if self.frame >= self.last_frame:
                if self.animating:
                    self.animating = False
                    self.frame_number = 0 #this should change
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

            self.set_hitbox(x,y)
            #^this has to be here or nothing works

            


    def move(self, dx, dy, x, y):
        self._setx(x + dx)
        self._sety(y + dy)
        return (self._getx(), self._gety())
        #and the hitbox will be updated in the update() method

    def movement(self, mode, x, y):
        #making sure the character moves gradually when animating
        if mode == "right":
            return self.move(7.5,0, x, y) 

        if mode == "left":
            return self.move(-7.5,0, x, y) 

        if mode == "jump":
            return self.move(0, -3, x, y) 

        if mode == "down":
            try:
                down_value = self.values[2]
            except: # values not set
                down_value = 5
                
            return self.move(0, down_value, x, y) #originally 4.18

            
#setting the first and last frames for each action usng the spritesheet notes
#the frist frames don't show on screen so ive set the frist frame to the previous last frame
    def default(self):
        if self.frame == 25:
            self.in_air = False
        self.frame = 0
        self.last_frame = 3
        self.default_mode = True
        #reset atributes
        self.first_frame = 0
        self.attack_box_row = -1
        self.blocking = False
        self.attacking = False
        self.being_attacked = False
        self.low = False
        self.high_attack = False
        
        
    def crouch(self):
        self.frame = 3
        self.last_frame = 6
        self.animating = True
        self.default_mode = False
        self.low = True
        self.frame_number = 0

    def block(self):
        self.frame = 7
        self.last_frame = 10
        self.animating = True
        self.default_mode = False
        self.blocking = True
        self.frame_number = 0

    def move_right(self):
        self.frame = 11
        self.last_frame = 14
        self.animating = True
        self.default_mode = False
        self.frame_number = 0

    def move_left(self):
        self.frame = 15
        self.last_frame = 17
        self.animating = True
        self.default_mode = False
        self.frame_number = 0

    def jump(self):
        self.frame = 18
        self.last_frame = 22
        self.animating = True
        self.default_mode = False
        self.in_air = True
        self.frame_number = 0

    def back_down(self):
        self.frame = 23
        self.last_frame = 25
        self.animating = True
        self.default_mode = False
        self.frame_number = 0

    def punch(self):
        self.frame = 26
        self.last_frame = 31
        self.animating = True
        self.default_mode = False
        self.attacking = True
        self.attack_box_row = 0
        self.frame_number = 0
        
    def kick(self):
        self.frame = 32
        self.last_frame = 36
        self.animating = True
        self.default_mode = False
        self.attacking = True
        self.attack_box_row = 1
        self.frame_number = 0
        
    def chop(self):
        self.frame = 37
        self.last_frame = 42
        self.animating = True
        self.default_mode = False
        self.attacking = True
        self.attack_box_row = 2
        self.frame_number = 0
        
    def low_punch(self):
        self.frame = 43
        self.last_frame = 47
        self.animating = True
        self.default_mode = False
        self.attacking = True
        self.low = True
        self.attack_box_row = 3
        self.frame_number = 0

    def low_kick(self):
        self.frame = 48
        self.last_frame = 53
        self.animating = True
        self.default_mode = False
        self.attacking = True
        self.low = True
        self.attack_box_row = 4
        self.frame_number = 0
        
    def low_block(self):
        self.frame = 54
        self.last_frame = 55
        self.animating = True
        self.default_mode = False
        self.low = True
        self.frame_number = 0
        
    def uppercut(self):
        self.frame = 56
        self.last_frame = 61
        self.animating = True
        self.default_mode = False
        self.attacking = True
        self.high_attack = True
        self.attack_box_row = 5
        self.frame_number = 0
        
    def high_kick(self):
        self.frame = 62 
        self.last_frame = 68
        self.animating = True
        self.default_mode = False
        self.attacking = True
        self.attack_box_row = 6
        self.frame_number = 0
        
    def hit(self):
        self.frame = 69
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
        return str(self.frame) + "," + str(self.first_frame) + \
                "," + str(self.last_frame) + "," + str(self.frame_width) + \
                "," + str(self.frame_height) + "," + str(self.columns) + \
                "," + str(self.rect)


class Goku(character):
    def __init__(self, target):
        character.__init__(self, "Goku", target)
        #each character has different values
        self.health = 100
        self.original_health = 100
        self.attack_power = 5
        self.defence = 5
        #getting the spritesheet
        path = os.path.join("spritesheets", "Goku", "GokuSheet.png")
        self.load(path, 95, 110, 75)
        self.default_height = 85

        #values
        self.default_y = 325
        self.highest_y = 270
        self.down_value = 6

        self.values = [self.default_y, self.highest_y, self.down_value]

    def set_box_lists(self,x ,y): #x,y needed for animation to work?
        #lists of hit boxes needed for that animation cycle a box for each frame is needed

        #--rect = x , y , width, height
        
        self.punch_boxes = [None,None, None, pygame.Rect((x + (self.hitbox_width-15)),(y + 45),10,10), None]
        self.kick_boxes = [None,pygame.Rect((x+70),(y+(self.hitbox_height - 45)),10,10),pygame.Rect((x+ 70),(y+(self.hitbox_height - 62)),10,10),None, None]
        self.chop_boxes = [None,None,None,pygame.Rect((x+(self.hitbox_width - 20)),(y+45),10,10),pygame.Rect((x+(self.hitbox_width - 20)),(y+45),10,10),None]
        self.low_punch_boxes = [None,None,pygame.Rect((x+(self.hitbox_width - 20)),(y+20),10,10),pygame.Rect((x+(self.hitbox_width - 18)),(y+20),10,10),None]
        self.low_kick_boxes = [None,None,pygame.Rect((x+(self.hitbox_width-15)),(y+ (self.hitbox_height + 10)),10,10),None,None,None]
        self.uppercut_boxes = [None,None,None,pygame.Rect((x+ (self.hitbox_width -20)),(y+50),10,10),pygame.Rect((x+(self.hitbox_width - 30)),(y+20),10,10),None]
        self.high_kick_boxes = [None,None,None,pygame.Rect((x+ (self.hitbox_width - 20)),(y+25),10,10),None,None,None]

        self.attack_boxes = [self.punch_boxes,
                             self.kick_boxes,
                             self.chop_boxes,
                             self.low_punch_boxes,
                             self.low_kick_boxes,
                             self.uppercut_boxes,
                             self.high_kick_boxes]
        

    def special_move(self):
        pass
        #move method unique to a character

class Raditz(character):
    def __init__(self,target):
        character.__init__(self, "Raditz", target)
        #each character has different values
        self.health = 100
        self.original_health = 100
        self.attack_power = 5
        self.defence = 5
        #getting the spritesheet
        path = os.path.join("spritesheets", "Raditz", "RaditzSheet.png")
        self.load(path, 112, 129, 75)

        #values
        self.default_y = 305
        self.highest_y = 250
        self.down_value = 5.5

        self.values = [self.default_y, self.highest_y, self.down_value]

    def set_box_lists(self,x,y):

        self.punch_boxes = [None,None, None, pygame.Rect((x + (self.hitbox_width-20)),(y + 55),10,10), None]
        self.kick_boxes = [None,pygame.Rect((x+80),(y+(self.hitbox_height - 55)),10,10),pygame.Rect((x+ 70),(y + 25),10,10),None, None] 
        self.chop_boxes = [None,None,None,pygame.Rect((x+(self.hitbox_width - 20)),(y+55),10,10),pygame.Rect((x+(self.hitbox_width - 20)),(y+45),10,10),None]
        self.low_punch_boxes = [None,None,pygame.Rect((x+(self.hitbox_width - 20)),(y+40),10,10),pygame.Rect((x+(self.hitbox_width - 22)),(y+40),10,10),None]
        self.low_kick_boxes = [None,None,pygame.Rect((x+(self.hitbox_width-20)),(y+ (self.hitbox_height + 20)),10,10),None,None,None] 
        self.uppercut_boxes = [None,None,None,pygame.Rect((x+ (self.hitbox_width - 20)),(y+60),10,10),pygame.Rect((x+(self.hitbox_width - 35)),(y+25),10,10),None]
        self.high_kick_boxes = [None,None,None,pygame.Rect((x+ (self.hitbox_width - 20)),(y+25),10,10),None,None,None]

        self.attack_boxes = [self.punch_boxes,
                             self.kick_boxes,
                             self.chop_boxes,
                             self.low_punch_boxes,
                             self.low_kick_boxes,
                             self.uppercut_boxes,
                             self.high_kick_boxes]
        


    
        
        

        

