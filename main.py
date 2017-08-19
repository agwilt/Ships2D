#!/usr/bin/env python3

import sys
import pygame
from pygame.locals import *

import ships, util
from colours import *
from classes import *
from config import *

def quit_game():
    pygame.display.quit()
    pygame.quit()
    sys.exit()

pygame.init()

# set up window
if SCREEN_FULLSCREEN:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN|ASYNCBLIT|HWSURFACE)
else:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), ASYNCBLIT|RESIZABLE|HWSURFACE)
pygame.display.set_caption("Ships 2D")

# set up water background
background = pygame.Surface(screen.get_size())
background = background.convert()
#bg_tile = pygame.image.load("water.png").convert()
#for y in range(0, SCREEN_HEIGHT, 32):
#    for x in range(0, SCREEN_WIDTH, 32):
#        background.blit(bg_tile, (x,y))
background.fill(SEA_BLUE)

# timing
clock = pygame.time.Clock()

# set up game?
ship_list = ShipGroup()
selected_ships = ShipGroup()

ship_list.add(ships.Dreadnought("HMS Dreadnought"))

# set zoom:
camera = Camera(0, 0, 4, 0)

ship_list.rotozoom(angle, zoom)

# main loop

screen.blit(background, (0,0))
pygame.display.flip()

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            quit_game()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4:
                if camera.zoom <= 16:
                    camera.zoom += 1
                ship_list.rotozoom(angle, zoom)
            if event.button == 5:
                if camera.zoom >= 2:
                    camera.zoom -= 1
                ship_list.rotozoom(angle, zoom)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit_game()

    keys=pygame.key.get_pressed()
    if keys[INPUT_CAMERA_CCW]:
        angle = (angle + 1)%360
        ship_list.setcamera(camera)
    if keys[INPUT_CAMERA_CW]:
        angle = (angle - 1)%360
        ship_list.setcamera(camera)

    ship_list.update()
    ship_list.clear(screen, background)
    ship_list.draw(screen)
    pygame.display.update()

    clock.tick(FPS)
