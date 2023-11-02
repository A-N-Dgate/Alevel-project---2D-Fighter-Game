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
