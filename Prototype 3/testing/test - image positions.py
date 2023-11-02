import pygame, os, sys

screen = pygame.display.set_mode((997,473))
pygame.display.set_caption("test - image positions")

path = os.path.join("spritesheets", "pre_level", "fight!.png")
test_image = pygame.image.load(path)

notes = """
win - (410,220)
lose - (410,220)
all at  (410,220)...
"""

while True:


            
    screen.blit(test_image, (410,220))
    pygame.display.update()
