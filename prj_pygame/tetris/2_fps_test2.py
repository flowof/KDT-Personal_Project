""" fps_test2.py """
import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((400,300))
FPSCLOCK = pygame.time.Clock()


def main():
    sysfont = pygame.font.SysFont(None, 36)
    counter = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        counter += 1
        SURFACE.fill((0,0,0))
        count_image = sysfont.render("count is {}".format(counter), True,(255,255,255))
        SURFACE.blit(count_image, (50,50)) #종이
        pygame.display.update()
        FPSCLOCK.tick(10) #초당 몇 번 업데이트 할 거냐


if __name__ == '__main__':
    main()
        
"""
pyGame의 문서
http://www.pygame.org/docs/
"""