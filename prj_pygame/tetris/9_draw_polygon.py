"""
ploygon(Surface, color, pointlist, width=0) -> Rect
Surface : 그리는 대상이 되는 화면(Surface 객체)
color : 색
pointlist : 점의 리스트
width : 선 폭(0일때는 꽉 채워 칠한다.)
"""

""" draw_polygon.py """
import sys
from math import sin, cos, radians
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((400, 300))
FPSCLOCK = pygame.time.Clock()


def main():

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        SURFACE.fill((0,0,0))

        pointlist0, pointlist1 = [], []
        for theta in range(0, 360, 72):
            rad = radians(theta)
            pointlist0.append((cos(rad)*100 + 100, sin(rad)*100 + 150))
            pointlist1.append((cos(rad)*100 + 300, sin(rad)*100 + 150))


        pygame.draw.lines(SURFACE, (255, 255, 255), True, pointlist0)
        pygame.draw.polygon(SURFACE, (255,255,255), pointlist1)

        pygame.display.update()
        FPSCLOCK.tick(30)

if __name__ == '__main__':
    main()
