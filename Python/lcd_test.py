# -*- coding: utf8 -*-

from time import sleep
import pygame, sys, os, time
from pygame.locals import *

import ht_01s
import ms5611
import cal_o2

pygame.init()

# set up the window
screen = pygame.display.set_mode((320, 240), 0, 32)
pygame.display.set_caption('Drawing')

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
CYAN  = (  0, 255, 255)
MAGENTA=(255,   0, 255)
YELLOW =(255, 255,   0)
 
# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BLACK)
#box = pygame.draw.rect(background, YELLOW,(40, 0, 40, 240))
#box = pygame.draw.rect(background,  CYAN, (80, 0, 40, 240))
#box = pygame.draw.rect(background, GREEN, (120, 0, 40, 240))
#box = pygame.draw.rect(background,MAGENTA,(160, 0, 40, 240))
#box = pygame.draw.rect(background, RED,   (200, 0, 40, 240))
#box = pygame.draw.rect(background, BLUE  ,(240, 0, 40, 240))
#box = pygame.draw.rect(background, BLACK ,(280, 0, 40, 240))

# Display some text
font_size = 36
row_sapce =30
font = pygame.font.Font(None, font_size)

    
screen.blit(background, (0, 0))
pygame.display.flip()
pygame.display.update()

running = True

ht01s = ht_01s.Ht_01s()
MS5611 = ms5611.Ms_5611()
oxy = cal_o2.Oxy_air()
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            running = False  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Pos: %sx%s\n" % pygame.mouse.get_pos())
            if textpos.collidepoint(pygame.mouse.get_pos()):
                pygame.quit()
                sys.exit()
                running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
    try:
        humi, temp2, status = ht01s.humi_temp_read()
        pressure, temp1 = MS5611.baro_read()
        air_oxy =oxy.cal_oxygen(temp1, humi, pressure)
        disp_v = [[("Temp1=%2.2f degC"%temp1),0,CYAN],
                  [("Humi=%2.2f %%"%humi),1,GREEN],
                  [("Temp2=%2.2f degC"%temp2),2,MAGENTA],
                  [("Press=%2.2f kPa"%pressure),3,YELLOW],
                  [("Air Oxy=%2.2f%%"%air_oxy),4,BLUE],
                  ]
        screen.fill(BLACK)
        for str_v, str_row, str_color  in disp_v:
            text_surface = font.render('%s'%str_v, True, str_color)        
            rect = text_surface.get_rect(topleft=(0,str_row*row_sapce))
            screen.blit(text_surface, rect)
        pygame.display.update()
        sleep(0.05)
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()
        running=False
    except:
        text = font.render("Sensor Connection Error!", 1, (BLACK))
        textpos = text.get_rect(centerx=background.get_width()/2,centery=background.get_height()/2)
        background.blit(text, textpos)
            