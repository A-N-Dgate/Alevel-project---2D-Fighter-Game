import pygame,math,random,os

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


class action_enemy(action):
    def __init__(self, name, movement, has_mode, mode):
        action.__init__(self, name, movement, has_mode, mode)
        self.priority = None

    def get_priority(self): return self.priority    
    def set_priority(self, a): self.priority = a
        

    def reset_priority(self):
        self.priority = None


class icon(pygame.sprite.Sprite):
    def __init__(self, character):
        pygame.sprite.Sprite.__init__(self)
        self.character = character
        self.outcome = None
        self.x = 0
        self.y = 0
        self.width = 60
        self.height = 60
        self.frame = 0
        self.last_time = 0
        self.rect = pygame.Rect(0,0,0,0)
        self.master_image = pygame.image.load(os.path.join("spritesheets", "characters", "%s" %(self.character.get_name()), "icon.png"))
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
        if self.outcome:
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

    def set_image_enemy(self, current_level,win):
        if self.character.get_level() < current_level:
            self.frame = 1
        elif self.character.get_level() == current_level and win:
            self.frame = 1
        elif self.character.get_level() == current_level and not win:
            self.frame = 0  
        else:
            self.frame = 0
             
        self.rect = pygame.Rect((self.width * self.frame),0,self.width,self.height)
        self.image = self.master_image.subsurface(self.rect)

    def set_rect_enemy(self): self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        


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



class kamehameha(ki_blasts):
    def __init__(self, character):
        ki_blasts.__init__(self, "kamehameha", character)
        self.frame = 0
        self.last_frame = 3
        self.rect = pygame.Rect(0,0,480,45)

        self.x = self.get_character()._getx() + self.character.hitbox_width 
        self.y = self.get_character()._gety() + 30

        #reallign special move for cell since he is taller
        if self.get_character().get_name() == "Cell":
            self.y += 20

    def update(self, screen):
        if self.get_character().get_frame() > 77:
        #^previous frames are getting the attack ready
            self._setx(self.character._getx() + self.character.hitbox_width)
            if not self.character.get_default_mode() and self.frame == 3:
                self.frame = 3
                if self.get_character().get_reversed():
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
                if self.get_character().get_reversed():
                    self.image = pygame.transform.flip(self.image, True, False)
                    self._setx(self._getx() - 550)
                self.hitbox = pygame.Rect(self.x, self.y, (120 * self.frame), 45)
                self.rect = self.hitbox
                self.old_frame = self.frame

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
        self.reversed = self.get_character().get_reversed()

        self.x = self.get_character()._getx() - 25
        self.y = self.get_character()._gety() - 150

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

            if self.reversed:
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
                self.kill()
                self.get_character().set_blast(False)
            else:
                self.get_character().set_blast(True)
                if self.get_character().get_frame() >= 85:
                    self.get_character().set_frame(85)
            
        if self.draw:
            self.group.draw(screen)
            

            

    def set_projectile(self):
        if not self.projectile and self.get_character().get_frame() >= 83:
            self.projectile = True

    def set_draw(self):
        if self.get_character().frame >= 78:
            self.draw = True


class galick_gun(ki_blasts):
    def __init__(self,character):
        ki_blasts.__init__(self, "galick_gun", character)
        self.frame = 0
        self.last_frame = 3
        self.rect = pygame.Rect(0,0,480,45)

        self.x = self.get_character()._getx() + self.character.hitbox_width 
        self.y = self.get_character()._gety() + 30

    def update(self,screen):
        if self.get_character().get_frame() > 78:
        #^previous frames are getting the attack ready
            self._setx(self.character._getx() + self.character.hitbox_width)
            if not self.character.get_default_mode() and self.frame == 3:
                self.frame = 3
                if self.get_character().get_reversed():
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
                if self.get_character().get_reversed():
                    self.image = pygame.transform.flip(self.image, True, False)
                    self._setx(self._getx() - 550)
                self.hitbox = pygame.Rect(self.x, self.y, (120 * self.frame), 45)
                self.rect = self.hitbox
                self.old_frame = self.frame
            
            self.group.draw(screen)

class shining_slash(ki_blasts):
    def __init__(self, character):
        ki_blasts.__init__(self, "shining_slash", character)
        self.old_frame = -1
        self.frame = -1
        self.last_frame = 1
        self.rect = pygame.Rect(0,0,85,75)
        #hitbox isnt't different (small difference in sizes but not much => ignore)

        self.get_character().set_attack_power(10)

        self.x = self.get_character()._getx() + self.character.hitbox_width 
        self.y = self.get_character()._gety() + 30

    def update(self, screen):
        if 83 < self.get_character().get_frame() < 88:
            #move character up
            self.get_character().movement("jump", self.get_character()._getx(), self.get_character()._gety(),False)
            
        elif 88 <= self.get_character().get_frame() < 90:
            #move character back down
            self.get_character().movement("down", self.get_character()._getx(), self.get_character()._gety(),False)
        
        elif self.get_character().get_default_mode() or self.frame > self.last_frame:
            #the blast is removed
            self.kill()
            self.get_character().set_blast(False)

        #drawing the blast onscreen
        elif self.get_character().get_frame() >= 103:

            
            #the blast gets updated
            if not self.get_character().get_reversed():
                self._setx(self._getx() + 20)
            else:
                self._setx(self._getx() - 20)
                
            if self.frame != self.last_frame:
                self.old_frame = self.frame
                self.frame += 1
                
            if self.frame != self.old_frame:
                self.rect = pygame.Rect((self.frame * 85), 0, 85,75)
                self.image = self.master_image.subsurface(self.rect)
                if self.get_character().get_reversed():
                    self.image = pygame.transform.flip(self.image, True, False)
                self.hitbox = pygame.Rect(self.x, self.y, 85,75)
                self.rect = self.hitbox
            self.group.draw(screen)

        else:     
            #set the hitbox on the tip of the sword - needs updated x and y values
            #list index = character frame number
            if not self.get_character().get_reversed():
                sword_hitboxes = [None,None,None,pygame.Rect((self.get_character()._getx() + 90),(self.get_character()._gety() + 50),(10),(10)),None,None,pygame.Rect((self.get_character()._getx() + 85),(self.get_character()._gety() + 45),10,10),None,None,None,None,None,None,None,None,pygame.Rect((self.get_character()._getx()+100),(self.get_character()._gety() + 60),10,10),pygame.Rect((self.get_character()._getx()+95),(self.get_character()._gety() + 80),10,10),None,None,None,None,None,None,None,None,None,None,None]
            else:
                sword_hitboxes = [None,None,None,pygame.Rect((self.get_character()._getx() + 10),(self.get_character()._gety() + 50),(10),(10)),None,None,pygame.Rect((self.get_character()._getx() + 5),(self.get_character()._gety() + 45),10,10),None,None,None,None,None,None,None,None,pygame.Rect((self.get_character()._getx()),(self.get_character()._gety() + 60),10,10),pygame.Rect((self.get_character()._getx()+5),(self.get_character()._gety() + 80),10,10),None,None,None,None,None,None,None,None,None,None,None]

            try:
                #sometimes the character's frame number isn't at the right value and therefore this section errors
                self.hitbox = sword_hitboxes[self.get_character().frame_number]
            except IndexError:
                pass
                

            

        
    

