""" draw_image_subregion1.py """
import sys
import pygame
from pygame.locals import QUIT, Rect


pygame.init()

SURFACE = pygame.display.set_mode((400, 200))
FPSCLOCK = pygame.time.Clock()


def main():

    logo = pygame.image.load("pythonlogo.jpg")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        SURFACE.fill((200,200,200))
        SURFACE.blit(logo, (0, 0))
        SURFACE.blit(logo,(250,50), Rect(0,0,200,100))

        pygame.display.update()
        FPSCLOCK.tick(30)

if __name__ == '__main__':
    main()
