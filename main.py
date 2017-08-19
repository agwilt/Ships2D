#!/usr/bin/env python3

import sys
import pygame
import math
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

d = ship_list.sprites()[0]

# set zoom:
camera = Camera(0, 0, 4, 0)

ship_list.setcamera(camera)

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
            if event.button == 5:
                if camera.zoom >= 2:
                    camera.zoom -= 1
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit_game()

    keys=pygame.key.get_pressed()
    if keys[INPUT_CAMERA_CCW]:
        camera.angle = (camera.angle + 1)%360
    if keys[INPUT_CAMERA_CW]:
        camera.angle = (camera.angle - 1)%360
    if keys[INPUT_CAMERA_LEFT]:
        camera.x -= 1
    if keys[INPUT_CAMERA_RIGHT]:
        camera.x += 1
    if keys[INPUT_CAMERA_UP]:
        camera.y -= 1
    if keys[INPUT_CAMERA_DOWN]:
        camera.y += 1
    if keys[INPUT_TURN_LEFT]:
        d.angle = (d.angle + 1)%360
    if keys[INPUT_TURN_RIGHT]:
        d.angle = (d.angle - 1)%360
    if keys[INPUT_MOVE_FRONT]:
        d.x += int(5 * math.cos(math.radians(d.angle)))
        d.y -= int(5 * math.sin(math.radians(d.angle)))
    if keys[INPUT_MOVE_BACK]:
        d.x -= int(5 * math.cos(math.radians(d.angle)))
        d.y += int(5 * math.sin(math.radians(d.angle)))

    #print("Status: Position %d, %d" % (d.turret_names['A'].x, d.turret_names['A'].y))
    #print("        Angle %d"  % d.angle)

    ship_list.setcamera(camera)

    ship_list.update()
    ship_list.clear(screen, background)
    ship_list.draw(screen)
    pygame.display.update()

    clock.tick(FPS)
