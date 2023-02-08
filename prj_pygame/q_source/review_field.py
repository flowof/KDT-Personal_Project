"""
테트리스 FIELD 만들기
WIDTH = 12
HEIGHT = 22
FIELD 초기화 (0)

"""

import sys
import pygame
#import time
from pygame.locals import QUIT

pygame.init()

SURFACE = pygame.display.set_mode([600,600])
pygame.display.set_caption('테트리스')
FPSCLOCK = pygame.time.Clock()

WIDTH = 12
HEIGHT = 12
FIELD = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
COLORS = ((0,0,0), (128,128,128))


def main():
    
    # smallfont = pygame.font.SysFont(None, 36)
    # largefont = pygame.font.SysFont(None, 72)
    # message_over = largefont.render("GAME TEST!!", True, (0,255,255))
    # message_rect = message_over.get_rect()
    # message_rect.center = (300,100)
    
    for ypos in range(HEIGHT):
        for xpos in range(WIDTH):
            FIELD[ypos][xpos] = 8 if xpos == 0  or xpos == WIDTH-1 else 0
            
    for index in range(WIDTH):
        FIELD[HEIGHT-1][index] = 8
    
    while True:
        SURFACE.fill((255,255,255))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # now = time.localtime()
        # str = '{0:04d}/{1:02d}/{2:02d} {3:02d}{4:02d}{5:02d}'.format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        # watch = smallfont.render(str, True, (0,255,0))
        # SURFACE.blit(watch, (300, 200))
        
        #SURFACE.blit(message_over, message_rect)
        
        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                val = FIELD[ypos][xpos]
                if val == 0:
                    pygame.draw.rect(SURFACE, COLORS[0], ((0,255,0), (xpos*25 +25, ypos*25 +25, 24, 24))
                if val == 8:
                    pygame.draw.rect(SURFACE, colors[1], (xpos*25 +25, ypos*25 +25, 24, 24))                 
        pygame.display.update()
        FPSCLOCK.tick(15)
     
if __name__ == '__main__':
    main()