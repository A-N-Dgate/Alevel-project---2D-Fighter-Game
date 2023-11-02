import pygame, sys, os, time
from animating_sprites import *

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
        self.original_health = 0
        #^for the health bars
        self.health_bar = None
        #^ set health bar when level is being set up

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
            y += self.hitbox_height // 2
            self.hitbox_height -= self.hitbox_height * 0.2

        if self.high_attack:
            y -= self.hitbox_height * 0.2

        if self.name == "Trunks":
            y -= 15
                
        self.hitbox = pygame.Rect(x,(y+(self.hitbox_height // 4)) , self.hitbox_width, self.hitbox_height)
        
        if self.attacking:
            self.set_attack_box(x,y)

    def get_attack_box(self): return self.attack_box
    def set_attack_box(self, x, y):
        self.set_box_lists(x, y)
        box_list = self.attack_boxes[self.attack_box_row]
        current_box = box_list[self.frame_number]
        self.attack_box = current_box

        if current_box != None:
            pygame.draw.rect(self.screen, (0,0,255), current_box, 2)

            
       
        
    def update(self,current_time, rate, x, y, mode): #, opposition - for set reversed
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

    def check_attack(self, opposition):
        if opposition.get_attack_box() != None and self.collide_rect(opposition) and not self.blocking and not self.being_attacked:
            self.set_health(self.get_health() - opposition.get_attack_power())
            self.hit()
            self.health_bar.character_hit()


    def collide_rect(self, opposition):
        #overwrite sprite collide rect
        return opposition.get_attack_box().colliderect(self.get_hitbox())
                
            
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
        self.select_x = 130

        self.values = [self.default_y, self.highest_y, self.down_value, self.select_x]

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
        self.select_x = 455
        
        self.values = [self.default_y, self.highest_y, self.down_value, self.select_x]

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
        self.health = 100
        self.original_health = 100
        self.attack_power = 5
        self.defence = 5
        #getting the spritesheet
        path = os.path.join("spritesheets", "Trunks", "TrunksSheet.png")
        self.load(path, 94, 91, 75)

        #values
        self.default_y = 344
        self.highest_y = 285
        self.down_value = 6.5
        self.select_x = 800
        
        self.values = [self.default_y, self.highest_y, self.down_value, self.select_x]

    def get_default_y(self): return self.default_y
    def get_highest_y(self): return self.highest_y
    def get_down_value(self): return self.down_value
    def get_select_x(self): return self.select_x

    def set_box_lists(self,x,y):
        # +15y from each
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


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------                
        

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


class selection_sprite(pygame.sprite.Sprite):
    def __init__(self, screen, character, image_path, x, y, num):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.character = character
        self.width = 300
        self.height = 453
        self.rect = pygame.Rect(x,y,self.width, self.height)
        self.image_rect = pygame.Rect((300 * num),0,self.width,self.height)
        self.master_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.master_image.subsurface(self.image_rect)
        self.character_position = ((self.rect.x // 2),(self.rect.y + self.height))
        
    def check_click(self, mouse_x, mouse_y):
        if self.x < mouse_x < (self.x + 300):
            return self.character

    def get_character_position(self): return self.character_position


class action():
    def __init__(self, name, movement, has_mode, mode):
        self.name = name
        self.mode = mode
        #boolean values
        self.movement = movement
        self.has_mode = has_mode

    #set once so it doesn't need set methods
    def get_name(self): return self.name
    def get_movement(self): return self.movement
    def get_has_mode(self): return self.has_mode
    def get_mode(self): return self.mode
    
        
        

        

