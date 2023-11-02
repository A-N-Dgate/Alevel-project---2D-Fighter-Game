import pygame, sys, time, random
from characterV3 import *

#test file but needs to be imported by enemy responces to be tested



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
        

def set_move_enemy():
    punch = action_enemy("punch", False, False, "")
    block = action_enemy("block", False, False, "")
    chop = action_enemy("chop", False, False, "")
    kick = action_enemy("kick", False, False, "")
    jump = action_enemy("jump", True, True, "jump")
    crouch = action_enemy("crouch", True, False, "")
    right = action_enemy("right", True, True, "right")
    left = action_enemy("left", True, True, "left")
    down = action_enemy("down", True, True, "down")
    default = action_enemy("default", False, False, "")

    return punch,block,chop,kick,jump,crouch,right,left,down,default



