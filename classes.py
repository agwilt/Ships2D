#!/usr/bin/env python3

import pygame
import math
from pygame.locals import *
from enum import Enum

import util

class Fuel(Enum):
    Sail = 0
    Coal = 1
    Oil = 2

class Camera():
    def __init__(self, x, y, zoom, angle):
        self.x = x
        self.y = y
        self.zoom = zoom
        self.angle = angle

#
# Abstract classes
#

class _Actor(pygame.sprite.Sprite):
    _image_name = ""

    def __init__(self):
        super().__init__()
        self.angle = 0
        self.x = 0
        self.y = 0

        self._image_orig = pygame.image.load(self._image_name).convert_alpha()
        self._length, self._width = self._image_orig.get_size()

    def setcamera(self, camera):
        # change zoom/rotation/position of camera
        # WARNING: camera only, this is purely to change the sprite and rect
        self.image = pygame.transform.scale(self._image_orig, (self._length*camera.zoom, self._width*camera.zoom))
        self.image = pygame.transform.rotate(self.image, self.angle - camera.angle)
        self.rect = self.image.get_rect()
        # set posision
        d = math.sqrt((self.x - camera.x)**2 + (self.y - camera.y)**2)
        beta = math.atan2((self.x - camera.x), (self.y - camera.y)) - camera.angle
        if self._image_name == "images/ships/HMS Dreadnought.bmp":
            print(beta)
        self.rect.centerx = camera.zoom * d * math.sin(beta)// 2
        self.rect.centery = camera.zoom * d * math.cos(beta)// 2



# a bit of sillyness:
class _SubActor(_Actor):
    def __init__(self, parent, pos_fore, pos_centre, base_angle):
        pygame.sprite.Sprite.__init__(self)

        self.parent = parent
        self.base_angle = base_angle # angle relative to parent (0° for forwards)
        self.pos_fore = pos_fore # distance along centreline, from middle [m]
        self.pos_centre = pos_centre # distance from centreline
        self.angle = 0
        self._image_orig = pygame.image.load(self._image_name).convert_alpha()
        self._length, self._width = self._image_orig.get_size()

    def __getattr__(self, name):
        if name == "x":
            if self.pos_centre == 0:
                return int(self.parent.x + self.pos_fore*math.cos(math.radians(self.parent.angle)))
            else:
                return int(self.parent.x + self.pos_fore*math.cos(math.radians(self.parent.angle)) - self.pos_centre*math.sin(math.radians(self.parent.angle)))
        elif name == "y":
            if self.pos_centre == 0:
                return int(self.parent.y - self.pos_fore*math.sin(math.radians(self.parent.angle)))
            else:
                return int(self.parent.y - self.pos_fore*math.sin(math.radians(self.parent.angle)) + self.pos_centre*math.cos(math.radians(self.parent.angle)))
        else:
            super().__getattr__(name)

    def __setattr__(self, name, value):
        if name == "x" or name == "y":
            raise AttributeError("can't set position of SubActor")
        else:
            super().__setattr__(name, value)

    def update_pos(self):
        # WARNING: converting pos_fore/centre to pixels
        self.rect.left = self.parent.rect.left + self.pos_fore*self.zoom
        self.rect.centery = self.parent.rect.centery + self.pos_centre*self.zoom

    def setcamera(self, camera):
        # add parent's angle
        super().setcamera(Camera(camera.x, camera.y, camera.zoom, camera.angle-self.base_angle-self.parent.angle))


#
# Game classes (actual objects will be subclasses)
#

class Turret(_SubActor):
    max_ammo = 80

    def __init__(self, parent, pos_fore, pos_centre, base_angle, max_langle, max_rangle):
        super().__init__(parent, pos_fore, pos_centre, base_angle)

        self.ammo = self.max_ammo
        self.health = 100 # 100: all fine, 0: useless, <100: slower

        self.max_langle = max_langle # relative to base
        self.max_rangle = max_rangle # relative to base


class Ship(_Actor):
    # Graphics:
    class_name = ""

    # Stats
    armour_deck = 0 # [mm]
    armour_belt = 0 # [mm]

    fuel_type = 0 # Fuel.something
    fuel_cap = 0 # capacity in tonnes
    fuel_cons = 0 # in tonnes / hour or something

    max_speed = 0 # [km/h]
    turn_rad = 0 # [m]

    dim_length = 160
    dim_beam = 25
    dim_draught = 9 # default: 9m for battleships/cruisers

#    belt_height = 3
#    arm_density = 7.8 # g/cm^3
#    belt_mass = self.armour_belt * (self.dim_length + self.dim_beam) * 2 * belt_height * arm_density
#    deck_mass = self.armour_deck * self.dim_length * self.dim_beam / 2
#    arm_mass = belt_mass + deck_mass
#    dry_mass = arm_mass # can compute this now. actual mass: dry+fuel+water

    displacement = dim_length * dim_draught * dim_beam / 2 # in tonnes
    max_mass = 1.5 * displacement # mass > max_mass: bad

    def __init__(self, name):
        self.name = name # HMS Thingy
        self.turrets = pygame.sprite.RenderUpdates()
        self.weapon_groups = [pygame.sprite.Group() for i in range(9)]

        self.res_fuel = self.fuel_cap
        self.res_water = 0 # taking on water? ..

        self.x = 0
        self.y = 0
        self.v_x = 0
        self.v_y = 0
        self.a = 0 # acceleration in direction of velocity
        self.a_turn = 0 # amount the ships is turning

        super().__init__()

        print("Loaded ship:", self.name)

    def mass(self):
        return self.dry_mass + self.res_fuel + self.res_water

    def setcamera(self, camera):
        super().setcamera(camera)
        # zoom turrets
        for turret in self.turrets.sprites():
            turret.setcamera(camera)

    def update(self):
        self.x += self.v_x
        self.y += self.v_y
        self.turrets.update()


class ShipGroup(pygame.sprite.Group):

    def draw(self, surface):
        super().draw(surface)
        for ship in self.sprites():
            ship.turrets.draw(surface)

    def clear(self, surface, background):
        super().clear(surface, background)
        for ship in self.sprites():
            ship.turrets.clear(surface, background)

    def setcamera(self, camera):
        for ship in self.sprites():
            ship.setcamera(camera)
