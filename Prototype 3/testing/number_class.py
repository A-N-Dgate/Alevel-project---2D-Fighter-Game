import pygame, sys, os

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


    


def set_timer(ticks):
    time = ticks
    return time

def check_timer(current_time, level_start_time):

##    #--------testing-------
##    print((current_time - level_start_time) // 1000)
##    #----------------------
    
    if current_time - level_start_time <= 300000: 
        #^ticks are in milliseconds
        return True
    else:
        return False


def get_time_remaining(current_time):
    time_remaining = 300 - (current_time // 1000)
    return time_remaining

def check_number_group(time_remaining, digit_1, digit_2, digit_3):
    if time_remaining < 100 and digit_1.alive():
        digit_1.kill()
        digit_2.set_digit(0)
        digit_3.set_digit(1)
        digit_2.set_x_value((digit_2.get_x_value() + 7))
        digit_3.set_x_value((digit_3.get_x_value() + 7))
    elif time_remaining < 10 and digit_2.alive():
        digit_2.kill()
        digit_3.set_digit(0)
        digit_3.set_x_value((digit_3.get_x_value() + 7))

    
        
        
        
