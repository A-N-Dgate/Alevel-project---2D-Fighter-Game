import pygame

def print_text(screen,  x, y, text, colour = (255,255,255)):
    font = pygame.font.Font(None, 18)
    imgText = font.render(text, True, colour)
    screen.blit(imgText, (x,y))
