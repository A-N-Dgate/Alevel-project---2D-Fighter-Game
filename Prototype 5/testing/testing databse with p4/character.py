import pygame, sys, os, time, random
from animating_sprites import *
from character_extras import *

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
        self.original_health = 0
        #^for the health bars
        self.health_bar = None
        #^ set health bar when level is being set up
        self.hold = False
        self.hold_frame = 0
        #^used for holding moves: crouch, block, left/right
        
        #---P4---
        self.ki_blast = None
        self.blast = False
        self.icon = icon(self.name)
        self.blast_hit = False
        
        

    def get_rect(self): return self.rect

    def get_health_bar(self): return self.health_bar
    def set_health_bar(self, a): self.health_bar = a

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

    def get_in_air(self): return self.in_air
    def get_low(self): return self.low
    def get_high_atack(self): return self.high_attack

    def set_hold(self,a): self.hold = a
    def get_hold(self): return self.hold


    def set_bool_reversed(self, a): self.reversed = a
            
    def get_original_health(self): return self.original_health
    def set_original_health(self, a): self.original_health = a

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

    #---
    def get_special_moves(self): return self.special_moves
    def get_icon(self): return self.icon

    def get_blast(self): return self.blast
    def set_blast(self, a): self.blast = a

    def get_frame(self):return self.frame
    def set_frame(self,a): self.frame = a

    def get_original_attack_power(self): return self.original_attack_power

    def get_blast_hit(self): return self.blast_hit
    def set_blast_hit(self, a): self.blast_hit = a
    #---

    #making sure that when the frame is updated, the hit box is updated as well
    def get_hitbox(self): return self.hitbox
    def set_hitbox(self, x, y):
        path = os.path.join("spritesheets", "characters", str(self.name), "dimensions.txt")
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
            y += self.hitbox_height // 2
            self.hitbox_height -= self.hitbox_height * 0.2

        if self.high_attack:
            y -= self.hitbox_height * 0.2

        if self.name == "Trunks":
            y -= 15

        if self.name == "Frieza" and self.reversed:
            x -= 30      
                
        self.hitbox = pygame.Rect(x,(y+(self.hitbox_height // 4)) , self.hitbox_width, self.hitbox_height)
        self.set_attack_box(x,y)

    def get_attack_box(self): return self.attack_box
    def set_attack_box(self, x, y):
        if self.blast:
            self.attack_box = self.ki_blast.get_hitbox()
        elif self.attacking:
            self.set_box_lists(x, y)
            box_list = self.attack_boxes[self.attack_box_row]
            try:
                current_box = box_list[self.frame_number]
                self.attack_box = current_box
            except: #sometimes the program is a bit behind to what is going on, so index out of range error
                pass


            
       
        
    def update(self,current_time, rate, x, y, mode, keydown): 
        #update the animation frame number
        self.old_frame = self.frame - 1
        if current_time > self.last_time + rate:
            if self.hold and self.frame == self.hold_frame:
            #freezes onto one frame if the move requires it
                self.hold_position(keydown)
            else:
                self.frame += 1
                self.frame_number += 1
            
            self.last_time = current_time
            if self.frame >= self.last_frame:
                if self.animating:
                    self.animating = False
                    self.frame_number = 0  
                else:
                    #default and defeated animations:
                    if self.frame > self.last_frame:
                        self.frame = self.first_frame

        #build on current frame only if it changed
        if self.frame != self.old_frame: 
            #gets current frame by covering up master image
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            self.rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(self.rect)
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
            
            if self.being_attacked and not self.attacking:
                if self.reversed:
                    self.move(1,0,x,y) 
                else:
                    self.move(-1,0,x,y)
            #^only works with an integer

            if self.blast:
                self.ki_blast.update(self.screen)
                if not self.ki_blast.alive():
                    self.ki_blast = None



    def move(self, dx, dy, x, y):
        self._setx(x + dx)
        self._sety(y + dy)
            
        return (self._getx(), self._gety())
        #and the hitbox will be updated in the update() method

    def movement(self, mode, x, y):
        #making sure the character moves gradually when animating
        if mode == "right":
            return self.move(7,0, x, y) 

        if mode == "left":
            return self.move(-7,0, x, y) 

        if mode == "jump":
            return self.move(0, -3, x, y) 

        if mode == "down":
            down_value = self.values[2]
            return self.move(0, down_value, x, y)

    def check_attack(self, opposition):
        if opposition.get_attack_box() != None and self.collide_rect(opposition) and not self.blocking and not self.being_attacked:
            self.set_health(self.get_health() - opposition.get_attack_power())
            self.hit()
            self.get_health_bar().character_hit()
            
            if opposition.get_blast():
                opposition.set_blast_hit(True)
            
        elif opposition.get_attack_box() != None and self.collide_rect(opposition) and self.blocking and not self.being_attacked:
            self.set_health(self.get_health() - (opposition.get_attack_power() // self.get_defence()))
            self.hit()
            self.get_health_bar().character_hit()

            if opposition.get_blast():
                opposition.set_blast_hit(True)


    def collide_rect(self, opposition):
        #overwrite sprite collide rect
        return opposition.get_attack_box().colliderect(self.get_hitbox())

    def hold_position(self, keydown):
        if keydown:
            self.frame = self.hold_frame
        else:
            self.hold = False
      
                
            
#setting the first and last frames for each action usng the spritesheet notes
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
        self.hold_frame = 0
        self.hold = False

        self.attack_box = None
        self.blast = False
        self.blast_hit = False
        if self.get_attack_power() != self.get_original_attack_power():
            self.set_attack_power(self.get_original_attack_power())
        
        
    def crouch(self):
        self.frame = 3
        self.last_frame = 6
        self.animating = True
        self.default_mode = False
        self.low = True
        self.frame_number = 0
        self.hold = True
        self.hold_frame = 5

    def block(self):
        self.frame = 7
        self.last_frame = 10
        self.animating = True
        self.default_mode = False
        self.blocking = True
        self.frame_number = 0
        self.hold = True
        self.hold_frame = 8

    def move_right(self):
        self.frame = 11
        self.last_frame = 14
        self.animating = True
        self.default_mode = False
        self.frame_number = 0
        self.hold = True
        self.hold_frame = 12

    def move_left(self):
        self.frame = 15
        self.last_frame = 17
        self.animating = True
        self.default_mode = False
        self.frame_number = 0
        self.hold = True
        self.hold_frame = 16

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
        self.attacking = False

        self.attack_box = None
        if self.get_attack_power() != self.get_original_attack_power():
            self.set_attack_power(self.get_original_attack_power())

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
        self.original_attack_power = 5
        self.defence = 5
        #getting the spritesheet
        path = os.path.join("spritesheets", "characters", "Goku", "GokuSheet.png")
        self.load(path, 95, 110, 83)
        #self.default_height = 85

        #values
        self.default_y = 325
        self.highest_y = 270
        self.down_value = 6
        self.select_x = 130

        self.values = [self.default_y, self.highest_y, self.down_value, self.select_x]
        self.special_moves = {"kamehameha":["punch", "chop", "move_right"]}

    def get_default_y(self): return self.default_y
    def get_highest_y(self): return self.highest_y
    def get_down_value(self): return self.down_value
    def get_select_x(self): return self.select_x

    def set_box_lists(self,x ,y): #x,y needed for animation to work?
        #lists of hit boxes needed for that animation cycle a box for each frame is needed

        if not self.reversed:
            self.punch_boxes = [None,None, None, pygame.Rect((x + (self.hitbox_width-15)),(y + 45),10,10), None]
            self.kick_boxes = [None,pygame.Rect((x+70),(y+(self.hitbox_height - 45)),10,10),pygame.Rect((x+ 70),(y+(self.hitbox_height - 62)),10,10),None, None]
            self.chop_boxes = [None,None,None,pygame.Rect((x+(self.hitbox_width - 20)),(y+45),10,10),pygame.Rect((x+(self.hitbox_width - 20)),(y+45),10,10),None]
            self.low_punch_boxes = [None,None,pygame.Rect((x+(self.hitbox_width - 20)),(y+20),10,10),pygame.Rect((x+(self.hitbox_width - 18)),(y+20),10,10),None]
            self.low_kick_boxes = [None,None,pygame.Rect((x+(self.hitbox_width-15)),(y+ (self.hitbox_height + 25)),10,10),None,None,None]
            self.uppercut_boxes = [None,None,None,pygame.Rect((x+ (self.hitbox_width -20)),(y+50),10,10),pygame.Rect((x+(self.hitbox_width - 30)),(y+20),10,10),None]
            self.high_kick_boxes = [None,None,None,pygame.Rect((x+ (self.hitbox_width - 20)),(y+25),10,10),None,None,None]

        if self.reversed:
            x -= self.hitbox_width
            
            self.punch_boxes = [None,None, None, pygame.Rect((x + (self.hitbox_width-17)),(y + 45),10,10), None]
            self.kick_boxes = [None,pygame.Rect((x+60),(y+(self.hitbox_height - 45)),10,10),pygame.Rect((x+ 60),(y+(self.hitbox_height - 62)),10,10),None, None]
            self.chop_boxes = [None,None,None,pygame.Rect((x+(self.hitbox_width - 30)),(y+45),10,10),pygame.Rect((x+(self.hitbox_width - 20)),(y+45),10,10),None]
            self.low_punch_boxes = [None,None,pygame.Rect((x+(self.hitbox_width - 20)),(y+20),10,10),pygame.Rect((x+(self.hitbox_width - 15)),(y+20),10,10),None]
            self.low_kick_boxes = [None,None,pygame.Rect((x+(self.hitbox_width-15)),(y+ (self.hitbox_height + 25)),10,10),None,None,None]
            self.uppercut_boxes = [None,None,None,pygame.Rect((x+self.hitbox_width),(y+55),10,10),pygame.Rect((x+(self.hitbox_width + 35)),(y+25),10,10),None]
            self.high_kick_boxes = [None,None,None,pygame.Rect((x+ (self.hitbox_width - 55)),(y+25),10,10),None,None,None]
            

        self.attack_boxes = [self.punch_boxes,
                             self.kick_boxes,
                             self.chop_boxes,
                             self.low_punch_boxes,
                             self.low_kick_boxes,
                             self.uppercut_boxes,
                             self.high_kick_boxes]
        

    def kamehameha(self):
        #move method unique to a character
        self.frame = 75
        self.last_frame = 82
        self.attacking = True
        self.default_mode = False
        self.animating = True
        self.blast = True
        self.ki_blast = kamehameha(self)
        
        


class Raditz(character):
    def __init__(self,target):
        character.__init__(self, "Raditz", target)
        #each character has different values
        self.health = 150
        self.original_health = 150
        self.attack_power = 2
        self.original_attack_power = 2
        self.defence = 7
        #getting the spritesheet
        path = os.path.join("spritesheets", "characters", "Raditz", "RaditzSheet.png")
        self.load(path, 112, 129, 75)

        #values
        self.default_y = 305
        self.highest_y = 250
        self.down_value = 5.5
        self.select_x = 455
        
        self.values = [self.default_y, self.highest_y, self.down_value, self.select_x]
        self.special_moves = {}

    def get_default_y(self): return self.default_y
    def get_highest_y(self): return self.highest_y
    def get_down_value(self): return self.down_value
    def get_select_x(self): return self.select_x

    def set_box_lists(self,x,y):
        if not self.reversed:
            self.punch_boxes = [None,None, None, pygame.Rect((x + (self.hitbox_width-20)),(y + 55),10,10), None]
            self.kick_boxes = [None,pygame.Rect((x+80),(y+(self.hitbox_height - 55)),10,10),pygame.Rect((x+ 70),(y + 25),10,10),None, None] 
            self.chop_boxes = [None,None,None,pygame.Rect((x+(self.hitbox_width - 20)),(y+55),10,10),pygame.Rect((x+(self.hitbox_width - 20)),(y+45),10,10),None]
            self.low_punch_boxes = [None,None,pygame.Rect((x+(self.hitbox_width - 20)),(y+40),10,10),pygame.Rect((x+(self.hitbox_width - 22)),(y+40),10,10),None]
            self.low_kick_boxes = [None,None,pygame.Rect((x+(self.hitbox_width-20)),(y+ (self.hitbox_height + 20)),10,10),None,None,None] 
            self.uppercut_boxes = [None,None,None,pygame.Rect((x+ (self.hitbox_width - 20)),(y+60),10,10),pygame.Rect((x+(self.hitbox_width - 35)),(y+25),10,10),None]
            self.high_kick_boxes = [None,None,None,pygame.Rect((x+ (self.hitbox_width - 20)),(y+25),10,10),None,None,None]

        if self.reversed:
            x -= self.hitbox_width

            self.punch_boxes = [None,None, None, pygame.Rect((x + (self.hitbox_width-10)),(y + 55),10,10), None]
            self.kick_boxes = [None,pygame.Rect((x+70),(y+(self.hitbox_height - 55)),10,10),pygame.Rect((x+ 75),(y + 25),10,10),None, None]
            self.chop_boxes = [None,None,pygame.Rect((x+70),(y+55),10,10),pygame.Rect((x+60),(y+55),10,10),None] 
            self.low_punch_boxes = [None,None,pygame.Rect((x+(self.hitbox_width - 40)),(y+35),10,10),pygame.Rect((x+(self.hitbox_width - 17)),(y+40),10,10),None]
            self.low_kick_boxes = [None,None,pygame.Rect((x+(self.hitbox_width-22)),(y+ (self.hitbox_height + 20)),10,10),None,None,None]
            self.uppercut_boxes = [None,None,None,pygame.Rect((x+self.hitbox_width-20),(y+60),10,10),pygame.Rect((x+(self.hitbox_width + 45)),(y+25),10,10),None] 
            self.high_kick_boxes = [None,None,None,pygame.Rect((x+60),(y+25),10,10),None,None,None] 
            

        self.attack_boxes = [self.punch_boxes,
                             self.kick_boxes,
                             self.chop_boxes,
                             self.low_punch_boxes,
                             self.low_kick_boxes,
                             self.uppercut_boxes,
                             self.high_kick_boxes]


class Trunks(character):
    def __init__(self,target):
        character.__init__(self, "Trunks", target)
        #each character has different values
        self.health = 120
        self.original_health = 120
        self.attack_power = 3
        self.original_attack_power = 3
        self.defence = 10
        #getting the spritesheet
        path = os.path.join("spritesheets", "characters", "Trunks", "TrunksSheet.png")
        self.load(path, 94, 91, 75)

        #values
        self.default_y = 344
        self.highest_y = 285
        self.down_value = 6.5
        self.select_x = 800
        
        self.values = [self.default_y, self.highest_y, self.down_value, self.select_x]
        self.special_moves = {}

    def get_default_y(self): return self.default_y
    def get_highest_y(self): return self.highest_y
    def get_down_value(self): return self.down_value
    def get_select_x(self): return self.select_x

    def set_box_lists(self,x,y):
        if not self.reversed:
            self.punch_boxes = [None,None, None, pygame.Rect((x + (self.hitbox_width-15)),(y + 50),10,10), None]
            self.kick_boxes = [None,pygame.Rect((x+70),(y+(self.hitbox_height - 40)),10,10),pygame.Rect((x + 55),(y+(self.hitbox_height - 70)),10,10),None, None]
            self.chop_boxes = [None,pygame.Rect((x+(self.hitbox_width- 20)),(y+50),10,10),None,None,pygame.Rect((x+(self.hitbox_width - 20)),(y+45),10,10),None]
            self.low_punch_boxes = [None,pygame.Rect((x+(self.hitbox_height + 5)),(y+22),10,10),pygame.Rect((x+(self.hitbox_width - 20)),(y+22),10,10),None,None]
            self.low_kick_boxes = [None,None,pygame.Rect((x+(self.hitbox_width-20)),(y+ (self.hitbox_height + 25)),10,10),None,None,None]
            self.uppercut_boxes = [None,None,None,pygame.Rect((x+ (self.hitbox_width-20)),(y+35),10,10),pygame.Rect((x+(self.hitbox_width - 50)),(y+35),10,10),None]
            self.high_kick_boxes = [None,None,None,pygame.Rect((x+ (self.hitbox_width - 30)),(y+20),10,10),None,None,None]

        if self.reversed: 
            x -= self.hitbox_width
            
            self.punch_boxes = [None,None, None, pygame.Rect((x + (self.hitbox_width-15)),(y + 50),10,10), None]
            self.kick_boxes = [None,pygame.Rect((x+60),(y+(self.hitbox_height - 40)),10,10),pygame.Rect((x+ 65),(y+(self.hitbox_height - 70)),10,10),None, None]
            self.chop_boxes = [None,pygame.Rect((x+(self.hitbox_width- 20)),(y+50),10,10),None,None,pygame.Rect((x+(self.hitbox_width - 10)),(y+45),10,10),None]
            self.low_punch_boxes = [None,pygame.Rect((x+(self.hitbox_height)),(y+22),10,10),pygame.Rect((x+(self.hitbox_width)),(y+22),10,10),None,None]
            self.low_kick_boxes = [None,None,pygame.Rect((x+(self.hitbox_width-20)),(y+ (self.hitbox_height + 25)),10,10),None,None,None]
            self.uppercut_boxes = [None,None,None,pygame.Rect((x+self.hitbox_width+15),(y+35),10,10),pygame.Rect((x+ self.hitbox_width + 50),(y+35),10,10),None]
            self.high_kick_boxes = [None,None,None,pygame.Rect((x+ (self.hitbox_width - 40)),(y+20),10,10),None,None,None]

        self.attack_boxes = [self.punch_boxes,
                             self.kick_boxes,
                             self.chop_boxes,
                             self.low_punch_boxes,
                             self.low_kick_boxes,
                             self.uppercut_boxes,
                             self.high_kick_boxes]
class Vegeta(character):
    def __init__(self,target):
        character.__init__(self, "Vegeta", target)
        #each character has different values
        self.health = 70
        self.original_health = 70
        self.attack_power = 10
        self.original_attack_power = 10
        self.defence = 3
        #getting the spritesheet
        path = os.path.join("spritesheets", "characters", "Vegeta", "VegetaSheet.png")
        self.load(path, 81, 97, 75)

        #values
        self.default_y = 340
        self.highest_y = 283
        self.down_value = 6
        self.select_x = 470

        self.values = [self.default_y, self.highest_y, self.down_value, self.select_x]
        self.special_moves = {}

    def get_default_y(self): return self.default_y
    def get_highest_y(self): return self.highest_y
    def get_down_value(self): return self.down_value
    def get_select_x(self): return self.select_x

    def set_box_lists(self,x ,y): 
        if not self.reversed:
            self.punch_boxes = [None,None, None, pygame.Rect((x + (self.hitbox_width-19)),(y + 45),10,10), None]
            self.kick_boxes = [None,None,pygame.Rect((x+ 50),(y+(self.hitbox_height - 65)),10,10),None, None] 
            self.chop_boxes = [None,None,None,pygame.Rect((x+(self.hitbox_width - 15)),(y+40),10,10),pygame.Rect((x+(self.hitbox_width - 20)),(y+40),10,10),None]
            self.low_punch_boxes = [None,None,pygame.Rect((x+(self.hitbox_width - 20)),(y+15),10,10),pygame.Rect((x+(self.hitbox_width - 18)),(y+20),10,10),None]
            self.low_kick_boxes = [None,None,pygame.Rect((x+(self.hitbox_width-15)),(y+ (self.hitbox_height + 5)),10,10),None,None,None]
            self.uppercut_boxes = [None,None,None,pygame.Rect((x+ (self.hitbox_width -20)),(y+50),10,10),pygame.Rect((x+(self.hitbox_width - 30)),(y+20),10,10),None]
            self.high_kick_boxes = [None,None,None,pygame.Rect((x+ (self.hitbox_width - 20)),(y+20),10,10),None,None,None]

        if self.reversed:
            x -= self.hitbox_width
            
            self.punch_boxes = [None,None, None, pygame.Rect((x + (self.hitbox_width-25)),(y + 45),10,10), None]
            self.kick_boxes = [None,None,pygame.Rect((x+ 55),(y+(self.hitbox_height - 65)),10,10),None, None]
            self.chop_boxes = [None,None,None,pygame.Rect((x+(self.hitbox_width - 30)),(y+40),10,10),pygame.Rect((x+(self.hitbox_width - 20)),(y+40),10,10),None]
            self.low_punch_boxes = [None,None,pygame.Rect((x+(self.hitbox_width - 15)),(y+15),10,10),pygame.Rect((x+(self.hitbox_width - 5)),(y+20),10,10),None]
            self.low_kick_boxes = [None,None,pygame.Rect((x+(self.hitbox_width-20)),(y+ (self.hitbox_height + 5)),10,10),None,None,None]
            self.uppercut_boxes = [None,None,None,pygame.Rect((x+(self.hitbox_width - 5)),(y+45),10,10),pygame.Rect((x+(self.hitbox_width + 30)),(y+20),10,10),None]
            self.high_kick_boxes = [None,None,None,pygame.Rect((x+ (self.hitbox_width - 45)),(y+20),10,10),None,None,None]
            

        self.attack_boxes = [self.punch_boxes,
                             self.kick_boxes,
                             self.chop_boxes,
                             self.low_punch_boxes,
                             self.low_kick_boxes,
                             self.uppercut_boxes,
                             self.high_kick_boxes]



#---new character
class Frieza(character):
    def __init__(self,target):
        character.__init__(self, "Frieza", target)
        self.health = 150
        self.original_health = 150
        self.attack_power = 15
        self.original_attack_power = 12
        self.defence = 1
        #getting the spritesheet
        path = os.path.join("spritesheets", "characters","Frieza", "FriezaSheet.png")
        self.load(path, 80, 81, 88)

        #values
        self.default_y = 355
        self.highest_y = 288 #298
        self.down_value = 5
        self.select_x = 0

        self.values = [self.default_y, self.highest_y, self.down_value, self.select_x]
        self.special_moves = {"death_ball":["punch", "kick", "jump"]}
        

    def get_default_y(self): return self.default_y
    def get_highest_y(self): return self.highest_y
    def get_down_value(self): return self.down_value
    def get_select_x(self): return self.select_x

    def set_box_lists(self,x ,y): 

        if not self.reversed:
            self.punch_boxes = [None,None, None, pygame.Rect((x + (self.hitbox_width-15)),(y + 35),10,10), None]
            self.kick_boxes = [None,None,pygame.Rect((x+ 50),(y+(self.hitbox_height - 62)),10,10),None, None]
            self.chop_boxes = [None,None,None,pygame.Rect((x+(self.hitbox_width - 20)),(y+35),10,10),pygame.Rect((x+(self.hitbox_width - 20)),(y+35),10,10),None]
            self.low_punch_boxes = [None,None,pygame.Rect((x+(self.hitbox_width - 20)),(y+15),10,10),pygame.Rect((x+(self.hitbox_width - 18)),(y+20),10,10),None]
            self.low_kick_boxes = [None,None,pygame.Rect((x+(self.hitbox_width-20)),(y + self.hitbox_height - 15),10,10),None,None,None]
            self.uppercut_boxes = [None,None,None,pygame.Rect((x+ (self.hitbox_width -20)),(y+40),10,10),pygame.Rect((x+(self.hitbox_width - 50)),(y+15),10,10),None]
            self.high_kick_boxes = [None,None,None,pygame.Rect((x+ (self.hitbox_width - 20)),(y+15),10,10),None,None,None]

        if self.reversed:
            x -= self.hitbox_width
            
            self.punch_boxes = [None,None, None, pygame.Rect((x+40),(y + 35),10,10), None]
            self.kick_boxes = [None,None,pygame.Rect((x+ 50),(y+(self.hitbox_height - 62)),10,10),None, None]
            self.chop_boxes = [None,None,None,pygame.Rect((x+(self.hitbox_width - 30)),(y+35),10,10),pygame.Rect((x+(self.hitbox_width - 20)),(y+35),10,10),None]
            self.low_punch_boxes = [None,None,pygame.Rect((x+40),(y+15),10,10),pygame.Rect((x+(self.hitbox_width - 15)),(y+15),10,10),None]
            self.low_kick_boxes = [None,None,pygame.Rect((x+(self.hitbox_width-15)),(y+ (self.hitbox_height - 15)),10,10),None,None,None]
            self.uppercut_boxes = [None,None,None,pygame.Rect((x+self.hitbox_width),(y+35),10,10),pygame.Rect((x+(self.hitbox_width + 15)),(y+15),10,10),None]
            self.high_kick_boxes = [None,None,None,pygame.Rect((x+ (self.hitbox_width - 25)),(y+15),10,10),None,None,None]
            

        self.attack_boxes = [self.punch_boxes,
                             self.kick_boxes,
                             self.chop_boxes,
                             self.low_punch_boxes,
                             self.low_kick_boxes,
                             self.uppercut_boxes,
                             self.high_kick_boxes]

    def death_ball(self):
        self.frame = 75
        self.last_frame = 87
        self.attacking = True
        self.default_mode = False
        self.animating = True
        self.blast = True
        #self.attack_power = 50
        self.ki_blast = death_ball(self)



class Enemy(character):
    def __init__(self,name, target):
        character.__init__(self,name, target)
        self.name = name
        self.queue = ["","","",""]
        self.detectbox_width = 0
        self.detectbox_height = 0
        self.s_detectbox_height = 0
        self.s_detectbox_width = 0
        self.value = 0
        self.detect_box = pygame.Rect(0,0,self.detectbox_width, self.detectbox_height)
        self.smaller_detectbox = pygame.Rect(0,0,self.s_detectbox_width, self.s_detectbox_height)
        self.level = 0

    def update(self,current_time, rate, x, y, mode, keydown):
        super().update(current_time, rate, x, y, mode, keydown)
        self.set_detect_box(x,y)
        self.set_smaller_detectbox(x,y)

    def get_detect_box(self): return self.detect_box
    def set_detect_box(self,x,y):
        self.detectbox_width = self.hitbox_width + self.value
        self.detectbox_height = self.hitbox_height + self.value
        

    def get_smaller_detectbox(self): return self.smaller_detectbox
    def set_smaller_detectbox(self,x,y):
        self.s_detectbox_width = self.hitbox_width + 20 
        self.s_detectbox_height = self.hitbox_height + 20



    def check_player_position(self, player):
        return player.get_hitbox().colliderect(self.get_detect_box())

    def close_contact_check(self, player):
        return player.get_hitbox().colliderect(self.get_smaller_detectbox())

    def get_queue(self): return self.queue

    def get_level(self): return self.level

        


class Raditz_enemy(Enemy, Raditz):
    def __init__(self, target):
        Enemy.__init__(self,"Raditz", target)
        Raditz.__init__(self,target)
        self.value = 160
        self.level = 1

    def set_detect_box(self,x ,y):
        Enemy.set_detect_box(self,x,y)
        y -= 50
        
        if self.reversed:
            x -= 30
        else:
            x -= 70
  
        self.detect_box = pygame.Rect(x,y,self.detectbox_width, self.detectbox_height)

    def set_smaller_detectbox(self,x,y):
        Enemy.set_smaller_detectbox(self,x,y)
        
        y += 10
        if self.reversed:
            x += 32
        else:
            x -= 10
        #^detectbox allignment needs to be perfect 

        self.smaller_detectbox = pygame.Rect(x,y,self.s_detectbox_width, self.s_detectbox_height)
        
        

    def set_queue(self, moves, player):
        #set moves and repeat moves
        punch,block,chop,kick,jump,crouch,right,left,down,default = moves
        kick_repeat = None
        punch_repeat = None

        chance = random.uniform(0,1)

        #move towards player
        if not self.check_player_position(player):
            if not self.reversed:
                right.set_priority(0)
            else:
                left.set_priority(0)
            default.set_priority(1)

        
        #to stop the enemy from attacking when the player-
        #- has left the smaller detection box
        if self.check_player_position(player):
            default.set_priority(0)

        #respond to the player
        if self.close_contact_check(player) and chance > 0.4:
            right.reset_priority()
            left.reset_priority()
            default.reset_priority()
            kick_repeat = kick
            kick.set_priority(0)
            kick_repeat.set_priority(1)
            crouch.set_priority(2)
            default.set_priority(3)
            
            if self.get_health() <= (self.get_original_health() // 4):
                kick_repeat.reset_priority()
                kick.reset_priority()
                crouch.reset_priority()

                #move away from player
                if self.reversed:
                    right.set_priority(0)
                else:
                    left.set_priority(0)
                default.set_priority(1)

        #after all the moves have had their priority set
        moves_ = [punch,block,chop,kick,jump,crouch,right,left,down,default]
        if punch_repeat != None:
            moves_.append(punch_repeat)
        if kick_repeat != None:
            moves_.append(kick_repeat)
            
        #set the queue
        for action in moves_:
            if action.get_priority() != None:
                try:
                    self.queue[action.get_priority()] = action
                except: #priority too low to fit into queue 
                    pass

        while len(self.queue) < 4:
            self.queue.append("")

        if self.queue[0] == "":
            self.queue[0] = moves[0]

        for x in moves:
            x.reset_priority()



class Frieza_enemy(Enemy, Frieza):
    def __init__(self, target):
        Enemy.__init__(self, "Frieza", target)
        Frieza.__init__(self,target)
        self.value = 180
        self.level = 2

    def set_detect_box(self,x,y):
        #done
        Enemy.set_detect_box(self,x,y)
        y -= 30
        if self.reversed:
            x -= 70
        else:
            x -= 70
  
        self.detect_box = pygame.Rect(x,y,self.detectbox_width, self.detectbox_height)

    def set_smaller_detectbox(self,x,y):
        #done not reversed
        Enemy.set_smaller_detectbox(self,x,y)
        
        y += 10
        if self.reversed:
            x = x
        else:
            x -= 10
        #^detectbox allignment needs to be perfect 

        self.smaller_detectbox = pygame.Rect(x,y,self.s_detectbox_width, self.s_detectbox_height)
        

    def set_queue(self, moves, player):
        punch,block,chop,kick,jump,crouch,right,left,down,default = moves
        kick_repeat = None
        punch_repeat = None

        chance = random.uniform(0,1)

        if self.check_player_position(player):
            if chance < 0.2:
                punch.set_priority(0)
                punch_repeat = punch
                punch_repeat.set_priority(2)
                chop.set_priority(1)
                default.set_priority(3)
                
            elif 0.2 <= chance < 0.5 and self.close_contact_check(player):
                block.set_priority(0)
                default.set_priority(1) 
                
            elif chance >= 0.5 and not self.close_contact_check(player):
                if player.get_reversed():
                    left.set_priority(0)
                else:
                    right.set_priority(0)

        else:
            if chance > 0.7 and not self.check_player_position(player):
                #for specials moves: 3, 2, 1
                jump.set_priority(0)
                kick.set_priority(1)
                punch.set_priority(2)
            else:
                if player.get_reversed():
                    right.set_priority(0)
                else:
                    left.set_priority(0)
                

        if self.get_health() <= 40 and self.close_contact_check(player):
            if chance >= 0.5:
                block.set_priority(0)

        #after all the moves have had their priority set
        moves_ = [punch,block,chop,kick,jump,crouch,right,left,down,default]
        if punch_repeat != None:
            moves_.append(punch_repeat)
        if kick_repeat != None:
            moves_.append(kick_repeat)
            
        #set the queue
        for action in moves_:
            if action.get_priority() != None:
                try:
                    self.queue[action.get_priority()] = action
                except: #priority too low to fit into queue 
                    pass

        while len(self.queue) < 4:
            self.queue.append("")

        if self.queue[0] == "":
            self.queue[0] = moves_[9]

        for x in moves:
            x.reset_priority()
                
        
        



