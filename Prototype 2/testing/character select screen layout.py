import pygame, sys

pygame.init()
screen = pygame.display.set_mode((997,473))

x1 = 25
y1 = 110

x2 = 350
y2 = 110

x3 = 675
y3 = 110

width = 300
height = 323

object1 = pygame.Rect(x1, y1, width, height)
object2 = pygame.Rect(x2,y2,width,height)
object3 = pygame.Rect(x3,y3,width,height)


screen.fill((255,255,255))
pygame.draw.rect(screen, (255,0,0),object1)
pygame.draw.rect(screen, (255,0,0),object2)
pygame.draw.rect(screen, (255,0,0),object3)
pygame.display.update()
    

    
