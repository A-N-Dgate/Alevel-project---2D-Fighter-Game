import pygame, os

class selection_sprite(pygame.sprite.Sprite):
    def __init__(self, screen, image_path, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.width = 0
        self.height = 0
        #^overwritten in subclass initialise method

        #for switching image
        self.frame = 0
        self.image_rect = pygame.Rect((self.width * self.frame), 0, self.width, self.height)
        self.master_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.master_image.subsurface(self.image_rect)

    def set_frame(self,mouse_x,mouse_y):
        prev_frame = self.frame
        if self.check_click(mouse_x,mouse_y):
            self.frame = 1
            if prev_frame != self.frame:
                self.play_music()
        else:
            self.frame = 0
        
    def check_click(self, mouse_x, mouse_y):
        if self.x < mouse_x < (self.x + self.width) and self.y < mouse_y < (self.y + self.height):
            return True

    def update(self, mouse_x, mouse_y):
        self.set_frame(mouse_x,mouse_y)
        self.image = self.master_image.subsurface(self.image_rect)
        self.image_rect = pygame.Rect((self.width * self.frame), 0, self.width, self.height)

    def play_music(self):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join("sfx", "mouse_on.wav")))

class character_selection_sprite(selection_sprite):
    def __init__(self, screen, character, image_path, x, y):
        selection_sprite.__init__(self, screen,image_path, x, y)
        self.width = 300
        self.height = 353
        self.rect = pygame.Rect(x,y,self.width, self.height)
        self.character = character

    def check_click(self, mouse_x, mouse_y):
        if self.x < mouse_x < (self.x + self.width) and self.y < mouse_y < (self.y + self.height):
            return self.character


class menu_select_sprite(selection_sprite):
    def __init__(self, screen, image_path, x, y, width, height):
        selection_sprite.__init__(self, screen, image_path, x, y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x,y,self.width, self.height)


class unlockable_character_select_sprite(character_selection_sprite):
    def __init__(self, screen, character, image_path, x, y, character_unlocked):
        character_selection_sprite.__init__(self,screen,character,image_path,x,y)
        self.character_unlocked = character_unlocked

    def set_frame(self,mouse_x,mouse_y):
        prev_frame = self.frame
        if not self.character_unlocked:
            self.frame = 2
        elif self.check_click(mouse_x,mouse_y):
            self.frame = 1
            if prev_frame != self.frame:
                self.play_music()
        else:
            self.frame = 0

    def get_character_unlocked(self): return self.character_unlocked

    def check_click(self, mouse_x, mouse_y):
        if self.x < mouse_x < (self.x + self.width) and self.y < mouse_y < (self.y + self.height) and self.character_unlocked:
            return self.character

