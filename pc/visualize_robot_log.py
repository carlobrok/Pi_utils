import pygame
import time

pygame.init()

(width, height) = (800, 500)
screen = pygame.display.set_mode((width, height))
pygame.display.flip()

background_color = [255, 255, 255]

running = True
while running:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
            pygame.quit()

    screen.fill(background_color)
    pygame.display.update()
