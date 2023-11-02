"""
this code isn't to be ran unitil added in the
final version of this prototype, this file is
just going to be used for trying to figure out
how to reorganise the level function
"""



#the orginal function:
def level1(screen,player):
    screen.fill((255,255,255))
    backgrounds = load_level_background("1") 
    
    enemy = Raditz_enemy(screen)
    characters = [player,enemy]
    group = add_group(characters)
    
    health_bars = set_level_positions(screen,player, enemy)
    healthbar_group = add_group(health_bars)
    player_healthbar = health_bars[0]
    enemy_healthbar = health_bars[1]

    timer_numbers = set_digits()
    number_group = add_group(timer_numbers)

    end_text = get_endlevel_images()
    
    framerate = pygame.time.Clock()
    action_queue = []
    moves = set_move()
    counter_moves = set_move_enemy()

    play = True
    defeated = False
    time_left = True
    keydown = [False,False,False,False]
    level_start_time = set_timer(pygame.time.get_ticks())


    while not defeated and time_left and play:
        framerate.tick(30)
        ticks = pygame.time.get_ticks()

        action_queue, keydown = set_queue(action_queue, moves, player, keydown)
        keypressed = check_true(keydown)

        if not player.get_animating():
            player_mode, action_queue = character_reaction(player,action_queue)

        if not enemy.get_animating():
            enemy.set_queue(counter_moves, player)
            enemy_mode, queue = character_reaction(enemy, enemy.get_queue())

        stay_on_screen(player,enemy)
        check_attacks(player,enemy)

        time_remaining = get_time_remaining(ticks, level_start_time)
        check_number_group(time_remaining, timer_numbers[0], timer_numbers[1], timer_numbers[2])

        updatescreen_level(screen, backgrounds, player, enemy, ticks, group, number_group,healthbar_group, player_mode, enemy_mode, keypressed, time_remaining)

        time_left = check_timer(ticks, level_start_time,player,enemy)
        defeated = check_defeated(player,enemy)
        start_time = get_start_time(ticks, defeated, time_left)

    while not time_left and play:
        framerate.tick(30)
        ticks = pygame.time.get_ticks()

        play = time_out_update(screen, backgrounds, player, enemy, ticks, group, healthbar_group, start_time, end_text[2], time_remaining)
        if not play:
            return False
           
            
    while defeated and time_left and play:
        framerate.tick(30)
        ticks = pygame.time.get_ticks()
        play = character_defeated_update(screen, backgrounds, player, enemy, ticks, group,number_group, healthbar_group, start_time, end_text)
        
        if not play and player.get_dead():
            return False
        elif not play and enemy.get_dead():
            return True


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def setup_level1(player):
    screen.fill((255,255,255))
    backgrounds = load_level_background("1") 
    
    enemy = Raditz_enemy(screen)
    """
    the only thing which will change between levels would be which enemy
    is being set

    set enemy function with the level number as a parameter. the enemy
    subclasses will have an attribute of their level and that will be used
    to determine which enemy will be returned.
    """
    characters = [player,enemy]
    group = add_group(characters)
    
    health_bars = set_level_positions(screen,player, enemy)
    healthbar_group = add_group(health_bars)
    """
    set level positions procedure doesn't need to
    return the health bars; they can just be set as the player
    or enemy healthbar then when the healthbar is needed you can
    use player.get_healthbar()
    
    healthbars = [player.get_health_bar(), enemy.get_health_bar()]
    healthbar_group = add_group(healthbars)
    """

    timer_numbers = set_digits()
    number_group = add_group(timer_numbers)

    end_text = get_endlevel_images()
    
    framerate = pygame.time.Clock()
    action_queue = []
    moves = set_move()
    counter_moves = set_move_enemy()

    play = True
    defeated = False
    time_left = True
    keydown = [False,False,False,False]
    level_start_time = set_timer(pygame.time.get_ticks())
    """
    i might keep the above in the level procedure so that
    i don't need to return that amny things but im not
    sure
    """

    return characters, character_group, timer_numbers, number_group healthbar_group


def main_game():
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    action_queue, keydown = set_queue(action_queue, moves, player, keydown)
    keypressed = check_true(keydown)

    if not player.get_animating():
        player_mode, action_queue = character_reaction(player,action_queue)

    if not enemy.get_animating():
        enemy.set_queue(counter_moves, player)
        enemy_mode, queue = character_reaction(enemy, enemy.get_queue())

    stay_on_screen(player,enemy)
    check_attacks(player,enemy)

    time_remaining = get_time_remaining(ticks, level_start_time)
    check_number_group(time_remaining, timer_numbers[0], timer_numbers[1], timer_numbers[2])

    updatescreen_level(screen, backgrounds, player, enemy, ticks, group, number_group,healthbar_group, player_mode, enemy_mode, keypressed, time_remaining)

    time_left = check_timer(ticks, level_start_time,player,enemy)
    defeated = check_defeated(player,enemy)
    start_time = get_start_time(ticks, defeated, time_left)

    return time_left, defeated, start_time
    


